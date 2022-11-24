from flask_restful import Resource
from garden_api.db_config import get_db
from flask import jsonify

class NbMarket(Resource):
    	
#GET the number of market

	def get(self):
		from garden_api.models import Marche
		try:
			market = Marche.query.all()
			resp = jsonify([[len(market)]])
			resp.status_code = 200
			return resp
		
		except Exception as e:   #Exception = all native exceptions which do not get out of the systeme
			print(e)  
		