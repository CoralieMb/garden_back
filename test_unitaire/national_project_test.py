from garden_api import create_app
import json
from test_unitaire.Tools import TestGeneric

class NationalProjectTest(TestGeneric):

    def test_nb_national_project(self):
        client = self.app.test_client()
        rv = client.get('/national_project/nombre/')
        print(rv.json)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json, [[2]], "le nombre de projets nationaux est le bon")  # assertEqual() same as expect() in vue js

    def test_national_project_get(self):
        client = self.app.test_client()
        rv = client.get('/national_project/') # We test the route
        #print(rv.json)
        self.assertEqual(len(rv.json), 2, "le nombre de projets nationaux dans la liste n'est pas le bon") 
        string_response = json.dumps(rv.json)
        print(string_response)
        self.assertIn('GAR', string_response, "le projet national n'est pas présent dans la liste") 

    def test_national_project_add(self):
        client = self.app.test_client()
        data1 = {'lib_projet_nat': 'Edu'}
        response = client.post('/national_project/', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        print(response.json)
        self.assertEqual(response.json, {'id_projet_nat': 3, 'lib_projet_nat': 'Edu'})

    def test_national_project_edit(self):
        client = self.app.test_client()
        data2 = {'lib_projet_nat': 'DNMA 2'}
        response = client.put('/national_project/1', data=json.dumps(data2), headers={'Content-Type': 'application/json'})
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id_projet_nat': 1, 'lib_projet_nat': 'DNMA 2'}, 'le projet national a été modifié')
        
    
    