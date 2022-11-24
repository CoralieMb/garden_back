from garden_api import create_app
import json
from test_unitaire.Tools import TestGeneric

class PlateformTest(TestGeneric):
   
    def test_nb_plateforme(self):
        client = self.app.test_client()
        rv = client.get('/plateforme/nombre/')
        print(rv.json)
        self.assertEqual(rv.json, [[10]], "le nombre de plateforme n'est pas le bon")  # assertEqual() same as expect() in vue js

    def test_plateforme_get(self):
        client = self.app.test_client()
        rv = client.get('/plateforme/') # We test the route
        print(rv.json)
        self.assertEqual(len(rv.json), 10, "le nombre de plateforme dans la liste n'est pas le bon") 
        string_response = json.dumps(rv.json)
        self.assertIn("Skolengo", string_response, "la plateforme n'est pas présente dans la liste") 
    
    def test_plateforme_add(self):
        client = self.app.test_client()
        data1 = {'id_plateforme': 50, 'lib_plateforme_long': 'plateforme Coralie long', 'lib_plateforme_court': 'plateforme Coralie court', 'id_editeur': 5, 'etat': 0, 'id_type_projet_territorial': 1}
        response = client.post('/plateforme/', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        print(response.json)
        self.assertEqual(response.json, {'id_plateforme': 50, 'lib_plateforme_long': 'plateforme Coralie long', 'lib_plateforme_court': 'plateforme Coralie court', 'id_editeur': 5, 'etat': 0, 'id_type_projet_territorial': 1}, 'la plateforme a été ajouté')

    def test_plateforme_edit(self):
        client = self.app.test_client()
        data2 = {'lib_plateforme_long': 'Envole1', 'lib_plateforme_court': 'Envole1 test', 'id_editeur': '6', 'etat': 1, 'id_type_projet_territorial': 1}
        response = client.put('/plateforme/2', data=json.dumps(data2), headers={'Content-Type': 'application/json'})
        print(response.json)
        self.assertEqual(response.json, {'lib_plateforme_long': 'Envole1', 'lib_plateforme_court': 'Envole1 test', 'id_editeur': 6, 'etat': 1, 'id_type_projet_territorial': 1, 'id_plateforme': 2}, 'la plateforme n\'a pas été modifié')

   
        

    