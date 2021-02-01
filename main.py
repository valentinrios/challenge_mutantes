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
app.config['SQLALCHEMY_DATABASE_URI'] = 'replace'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
regex_check = r'([A,T,C,G])\1{3,3}'

'''
Clase que representa migracion de tabla "Dna" en base de datos.
'''
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

'''
Esquema de tabla "Dna" para acceder a los elementos de la misma.
'''
class DnaSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Dna
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    dna_string = fields.String(required=True)
    result = fields.Boolean(required=True)


'''
Clase que representa el servicio "/mutant"
'''
class Mutant(Resource):
    def post(self):

        def split(word): 
            return [char for char in word]

        '''
        Funcion principal para determinar si un el array de strings enviados es de un mutante o de un humano.
        Retorna True en caso de ser mutante y False en caso de ser humano.
        '''
        def is_mutant(dna):
            total_matchs = horizontal_matchs(dna) + vertical_matchs(dna) + diagonal_matchs(dna)
            if total_matchs > 1:
                return True
            else:
                return False
            
        '''
        Funcion secundaria para encontrar las coincidencias horizontales en adn.
        '''
        def horizontal_matchs(dna):
            matchs = 0
            for horizontal in dna:    
                match = re.search(regex_check, horizontal)
                if match is not None and match[0] != "":
                    matchs += 1
            return matchs

        '''
        Funcion secundaria para encontrar las coincidencias verticales en adn.
        '''
        def vertical_matchs(dna):
            verticals = []
            matchs = 0
            for i in range(len(dna)):
                temporal_string = ""
                for j in range(len(dna)):
                    temporal_string += dna[j][i]
                verticals.append(temporal_string)
                
            for vertical in verticals:    
                match = re.search(regex_check, vertical)
                if match is not None and match[0] != "":
                    matchs += 1
            return matchs

        '''
        Funcion secundaria para encontrar las coincidencias diagonales en adn.
        '''
        def diagonal_matchs(dna):
            aux=[]
            matchs = 0
            for dna_string in dna:
                #print(split(dna_string))
                aux.append(split(dna_string))
            x = np.array(aux)
            diagonals = [x[::-1,:].diagonal(i) for i in range(-3,4)]
            diagonals.extend(x.diagonal(i) for i in range(3,-4,-1))
            for diagonal in diagonals:    
                match = re.search(regex_check, ''.join(diagonal.tolist()))
                if match is not None and match[0] != "":
                    matchs += 1
            return matchs
        
        #Recepcion y tratamiento de argumentos recibidos.
        args = request.get_json()
        print(args['dna'])
        dna_strings = args['dna']

        #Llamado a funcion principal
        is_mutant = is_mutant(dna_strings)

        #Creacion de registro en base de datos
        dna_schema = DnaSchema()
        dna = dna_schema.load({"dna_string": str(args['dna']), "result": is_mutant})
        dna_schema.dump(dna.create())
        
        #Envio de respuesta
        if is_mutant == True:
            return jsonify({"result": is_mutant})
        else:
            abort(403, result=is_mutant)

'''
Clase que representa el servicio "/stats"
'''
class Stats(Resource):
    def get(self):
        mutant_count = db.session.query(Dna).filter(Dna.result == 1).count()
        human_count = db.session.query(Dna).filter(Dna.result == 0).count()
        ratio = round(mutant_count/human_count if human_count else 0, 2)
        return jsonify({"count_mutant_dna":mutant_count, "count_human_dna":human_count, "ratio":ratio})        

api.add_resource(Mutant, '/mutant') 
api.add_resource(Stats, '/stats') 

if __name__ == '__main__':
     app.run(host='0.0.0.0',port='5002')