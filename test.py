from main import app
import unittest
from flask import json

class IsMutantTestCase(unittest.TestCase):

    def test_is_mutant(self):
        tester = app.test_client(self)
        info = {"dna":["ATGCGAA","CCGTGCC","TTATGTA","AGAAGGA","CACCTAT","TCACTGT","TTTTTGT"]}
        response = tester.post('/mutant', data = json.dumps(info), headers={'Content-Type': 'application/json'})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_is_human(self):
        tester = app.test_client(self)
        info = {"dna":["ATGCGAA","CCGTGCC","TTATGTA","AGAAGGA","CACCTAT","TCACTGT","TTGTTGT"]}
        response = tester.post('/mutant', data = json.dumps(info), headers={'Content-Type': 'application/json'})
        statuscode = response.status_code
        self.assertEqual(statuscode, 403)

    def test_mutant_service_response(self):
        tester = app.test_client(self)
        info = {"dna":["ATGCGAA","CCGTGCC","TTATGTA","AGAAGGA","CACCTAT","TCACTGT","TTTTTGT"]}
        response = tester.post('/mutant', data = json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertTrue(b'result' in response.data)

    def test_stats_service_response_code(self):
        tester = app.test_client(self)
        response = tester.get('/stats')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_stats_service_response(self):
        tester = app.test_client(self)
        response = tester.get('/stats')
        self.assertTrue(b'count_human_dna' in response.data and b'count_mutant_dna' in response.data and b'ratio' in response.data)

if __name__ == "__main__":
    unittest.main()