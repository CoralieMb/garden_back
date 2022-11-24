from garden_api import create_app
import json
from test_unitaire.Tools import TestGeneric

class TerritorialProjectTypeTest(TestGeneric):

    def test_nb_territorial_project_type(self):
        client = self.app.test_client()
        rv = client.get('/territorial_project_type/nombre/')
        print(rv.json)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json, [[2]], "le nombre de type de projet territorial n'est pas le bon")  # assertEqual() same as expect() in vue js

    def test_territorial_project_type_get(self):
        client = self.app.test_client()
        rv = client.get('/territorial_project_type/') # We test the route
        #print(rv.json)
        self.assertEqual(len(rv.json), 2, "le nombre de type de projet territorial dans la liste n'est pas le bon") 
        string_response = json.dumps(rv.json)
        print(string_response)
        self.assertIn('PROJET_ENT', string_response, "le type de projet territorial n'est pas présent dans la liste") 

    def test_territorial_project_type_add(self):
        client = self.app.test_client()
        data1 = {'lib_type_projet_territorial': 'type projet test 2 long'}
        response = client.post('/territorial_project_type/', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        print(response.json)
        self.assertEqual(response.json, {'id_type_projet_territorial': 3, 'lib_type_projet_territorial': 'type projet test 2 long'})

    def test_territorial_project_type_edit(self):
        client = self.app.test_client()
        data2 = {'lib_type_projet_territorial': 'PROJET_GAR'}
        response = client.put('/territorial_project_type/1', data=json.dumps(data2), headers={'Content-Type': 'application/json'})
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id_type_projet_territorial': 1, 'lib_type_projet_territorial': 'PROJET_GAR'}, 'l\'exploitant a été modifié')
        
    
    