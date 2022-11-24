from garden_api import create_app
import json
from test_unitaire.Tools import TestGeneric

class MarketTest(TestGeneric):

    def test_nb_market(self):
            client = self.app.test_client()
            rv = client.get('/marche/nombre/')
            print(rv.json)
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json, [[1]], "le nombre de marché est le bon")  # assertEqual() same as expect() in vue js

    def test_market_get_test(self):
        client = self.app.test_client()
        rv = client.get('/marche/') # We test the route
        print(rv.json)
        self.assertEqual(len(rv.json), 2, "le nombre de marché dans la liste n'est pas le bon") 
        string_response = json.dumps(rv.json)
        print(string_response)
        # self.assertIn('Fourniture D\'Un Espace Numérique De Travail (Ent) Pour Les Collèges Du Var Et Les écoles Primaires De Toulon', string_response, "le marché est présent dans la liste") 