from flask import Flask, request
from flask_restful import Resource, Api, abort
from sqlalchemy import create_engine, func
from json import dumps
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import re
import numpy as np


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:BH3k9Ibr9dd4FFhE@localhost:3306/dna'
db = SQLAlchemy(app)
api = Api(app)

class Dna(db.Model):
    __tablename__ = "dna"
    id = db.Column(db.Integer, primary_key=True)
    dna_string = db.Column(db.String(2000))
    result = db.Column(db.Boolean)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,dna_string,result):
        self.dna_string = dna_string
        self.result = result
    def __repr__(self):
        return '' % self.id
db.create_all()

class DnaSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Dna
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    dna_string = fields.String(required=True)
    result = fields.Boolean(required=True)

class Mutant(Resource):
    def post(self):

        def split(word): 
            return [char for char in word]

        def isMutant(dna):
            total_matchs = horizontal_matchs(dna) + vertical_matchs(dna) + diagonal_matchs(dna)
            if total_matchs > 1:
                return True
            else:
                return False
            
        def horizontal_matchs(dna):
            matchs = 0
            for dna_string in dna:    
                match = re.search(r'([A,T,C,G])\1{3,3}', dna_string)
                if match is not None and match[0] != "":
                    matchs += 1
            return matchs

        def vertical_matchs(dna):
            verticals = []
            matchs = 0
            for i in range(len(dna)):
                temporal_string = ""
                for j in range(len(dna)):
                    temporal_string += dna[j][i]
                verticals.append(temporal_string)
                
            for vertical in verticals:    
                match = re.search(r'([A,T,C,G])\1{3,3}', vertical)
                if match is not None and match[0] != "":
                    matchs += 1
            return matchs

        def diagonal_matchs(dna):
            aux=[]
            matchs = 0
            for dna_string in dna:
                #print(split(dna_string))
                aux.append(split(dna_string))
            x = np.array(aux)
            diags = [x[::-1,:].diagonal(i) for i in range(-3,4)]
            diags.extend(x.diagonal(i) for i in range(3,-4,-1))
            for n in diags:    
                match = re.search(r'([A,T,C,G])\1{3,3}', ''.join(n.tolist()))
                if match is not None and match[0] != "":
                    matchs += 1
            return matchs
        
        args = request.args
        dna_strings = args['dna'].strip('][').replace('"', '').split(',')
        is_mutant = isMutant(dna_strings)
        dna_schema = DnaSchema()
        dna = dna_schema.load({"dna_string": args['dna'], "result": is_mutant})
        result = dna_schema.dump(dna.create())
        if is_mutant == True:
            return jsonify({"data": result})
        else:
            abort(403, error_message=result)


class Stats(Resource):
    def get(self):
        mutant_count = db.session.query(Dna).filter(Dna.result == 1).count() #db.session.execute("SELECT count(*) from dna.dna d where result = 1").scalar() #
        human_count = db.session.query(Dna).filter(Dna.result == 0).count()
        ratio = round(mutant_count/human_count, 2)
        return jsonify({"count_mutant_dna":mutant_count, "count_human_dna":human_count, "ratio":ratio})
        

api.add_resource(Mutant, '/mutant') # Route_1
api.add_resource(Stats, '/stats') # Route_2


if __name__ == '__main__':
     app.run(port='5002')