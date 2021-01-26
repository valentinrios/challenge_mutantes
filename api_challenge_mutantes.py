from flask import Flask, request
from flask_restful import Resource, Api, abort
from sqlalchemy import create_engine
from json import dumps
from flask.json import jsonify
import re
import numpy as np

db_connect = create_engine('sqlite:///D:/Users/Valentin/Documents/GitHub/repositories/challenge_mutantes/mutants.db')
app = Flask(__name__)
api = Api(app)

class Mutant(Resource):
    def post(self):
        # conn = db_connect.connect() # connect to database
        # query = conn.execute("select * from employees") # This line performs query and returns json result
        # return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
        
        def split(word): 
            return [char for char in word]

        def isMutant(dna):
            total_matchs = horizontal_matchs(dna) + vertical_matchs(dna) + diagonal_matchs(dna)
            if total_matchs >= 3:
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
        
        # dna =  ["ATGCGAA",
        #         "CAGTGCA",
        #         "TTATGTA",
        #         "AGAAGGA",
        #         "CCCCTAT",
        #         "TCACTGT",
        #         "TTTTTGT"]
        args = request.args
        print (args) # For debugging
        dna = args['dna'].strip('][').replace('"', '').split(',')
        print(dna)
        cur = db_connect.connect()
        is_mutant = isMutant(dna)
        if is_mutant == True:
            sql =  "INSERT INTO dna(dna_string,result) VALUES('" + args['dna'] + "','"+ str(is_mutant) +"')" 
            cur.execute(sql)
            return jsonify(dict(data=[True,"Is a mutant!"]))
        else:
            abort(403, error_message='Is not a mutant!')


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
        

api.add_resource(Mutant, '/mutant') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')