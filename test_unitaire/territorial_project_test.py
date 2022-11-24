from garden_api import create_app
import json
from test_unitaire.Tools import TestGeneric


class TerritorialProjectTest(TestGeneric):

    def test_project_territorial_nb(self):
        client = self.app.test_client()
        rv = client.get('/projet_territorial_uai/nombre/')
        # print(rv.json)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json, [[11]],
                         "le nombre de projet n'est pas le bon")  # assertEqual() same as expect() in vue js

    def test_project_territorial_get(self):
        client = self.app.test_client()
        rv = client.get('/projet_territorial_uai/')  # We test the route
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(len(rv.json), 11, "le nombre de projet dans la liste n'est pas le bon")
        string_response = json.dumps(rv.json)
        # print(string_response)
        self.assertIn('@Ucollege84', string_response, "le projet n'est pas présent dans la liste")

    def test_project_territorial_add(self):
        client = self.app.test_client()
        data1 = {'id_projet_territorial_uai': 11, 'lib_projet_territorial_uai_long': 'projet test 2 long', 'lib_projet_territorial_uai_court': 'projet test 2 court',
                 'id_type_projet_territorial': 1}
        response = client.post('/projet_territorial_uai/', data=json.dumps(data1), headers={'Content-Type': 'application/json'})
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'id_projet_territorial_uai': 11, 'lib_projet_territorial_uai_long': 'projet test 2 long', 'lib_projet_territorial_uai_court': 'projet test 2 court',
                 'id_type_projet_territorial': 1},
                         'le projet n\'a pas été ajouté')

    def test_project_territorial_edit(self):
        client = self.app.test_client()
        data2 = {'lib_projet_territorial_uai_long': 'Chercan', 'lib_projet_territorial_uai_court': 'Chercan test',
                 'id_type_projet_territorial': 1}
        response = client.put('/projet_territorial_uai/4', data=json.dumps(data2), headers={'Content-Type': 'application/json'})
        # print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'id_projet_territorial_uai': 4, 'lib_projet_territorial_uai_long': 'Chercan', 'lib_projet_territorial_uai_court': 'Chercan test',
                 'id_type_projet_territorial': 1},
                         'le projet n\'a pas été modifié')


