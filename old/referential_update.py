from flask_restful import Resource
from .db_config import get_db
from flask import jsonify, request 

import os
from os.path import join, dirname, realpath
import pandas as pd
import csv


''' class Effectif(Resource):
	def post(self):
		uploaded_file = request.files['file']
		if uploaded_file.filename != '':
			return add(uploaded_file,'effectif',['periode', 'profil', 'niveau','effectif']) 
		else:
			resp = jsonify('Fichier inconnu')
			resp.status_code = 400
		return resp	
	
	def put(self):
		uploaded_file = request.files['file']
		if uploaded_file.filename != '':
			return update(uploaded_file,'effectif',['periode', 'profil', 'niveau','effectif']) 
		else:
			resp = jsonify('Fichier inconnu')
			resp.status_code = 400
		return resp	

api.add_resource(Effectif, '/insert_effectif/') '''


class Deploiement(Resource):
    
# Add new element
	def post(self):
		uploaded_file = request.files['file']
		#if the file exist
		if uploaded_file.filename != '':
			return self.modify(uploaded_file,'deploiement_projet_territorial_uai',['uai', 'lib_projet_territorial_uai_court', 'lib_plateforme_court','debut_deploiement', 'fin_deploiement']) 
		else:
			resp = jsonify('Fichier inconnu')
			resp.status_code = 400
		return resp

# Update an element
	''' def put(self):
		uploaded_file = request.files['file']
		#if the file exist
		if uploaded_file.filename != '':
			return self.update(uploaded_file,'deploiement_projet_territorial_uai',['uai', 'lib_projet_territorial_uai_court', 'lib_plateforme_court','debut_deploiement', 'fin_deploiement']) 
		else:
			resp = jsonify('Fichier inconnu')
			resp.status_code = 400
		return resp '''

	# function which add new items
	def modify(self, file_path, table_name,fieldnames):
		try:
			conn = get_db()
			# CVS Column Names
			# Use Pandas to parse the CSV file
			csv_data = csv.DictReader(file_path, delimiter=";") # on peut mettre les noms des champs en 2ème paramètre pour récupérer que cela
			# Loop through the Rows
			success_nb =0
			
			for row in csv_data:
				try:
					cursor = conn.cursor()
					fieldlist = ",".join([fieldname for fieldname in fieldnames])
					field_param = ",".join(["%s"] *len(fieldnames))
					# if (Ajout)
					sql = f"INSERT INTO {table_name} ({fieldlist}) VALUES ({field_param})"

					# if (Modifier)

					sql = f"UPDATE {table_name} SET uai=%s, id_projet_territorial_uai=%s, id_plateforme=%s, date_debut=%s, date_fin=%s, commentaire=%s WHERE uai=%s"
					
					#ne fonctionne pas à partir d'ici
					data = list(row[fieldname] for fieldname in fieldnames)
					
					cursor.execute(sql, data)
					print(cursor.lastrowid) 
					conn.commit()
					success_nb+=1
					
				except Exception as erreur_db:
					print("erreur")
					print(erreur_db)
			resp = jsonify('Nombre de succès : %d' % success_nb)
			resp.status_code = 201

		except Exception as e:
			print(e)
			resp = jsonify('Echec de l\'ajout dans la BDD')
			resp.status_code = 400

		finally:
			cursor.close()
			
		return resp

	# function which update items
	def update(self, file_path, table_name,fieldnames):
		try:
			conn = get_db()
			# CVS Column Names
			# Use Pandas to parse the CSV file
			csv_data = csv.DictReader(file_path, delimiter=";")
			# Loop through the Rows
			success_nb =0
			
			for row in csv_data:
				try:
					cursor = conn.cursor()
					sql = f"UPDATE {table_name} SET uai=%s, id_projet_territorial_uai=%s, id_plateforme=%s, date_debut=%s, date_fin=%s, commentaire=%s WHERE uai=%s"

					data = list(row[fieldname] for fieldname in fieldnames) 

					#get the uai value for the "uai = %s" and add it in data
					data_uai= data[0]
					data.append(data_uai)

					# data_final is all the value of the row + uai value at the end
					data_final = data
					
					#cursor.execute(sql, data_final)
					conn.commit()
					success_nb+=1
					print(success_nb)
			
				except Exception as erreur_db:
					print(erreur_db)
			resp = jsonify('Nombre de succès : %d' % success_nb)
			resp.status_code = 201

		except Exception as e:
			print(e)
			resp = jsonify('Echec de l\'ajout dans la BDD')
			resp.status_code = 400

		finally:
			cursor.close()
			
		return resp


	''' def commandline_insert (filename):
			with open(filename,"r") as file_csv:
				print(update(file_csv, "deploiement_projet_territorial_uai", ['uai', 'id_projet_territorial_uai', 'id_plateforme', 'date_debut', 'date_fin', 'commentaire'])) '''

	#if __name__ == '__main__':
		#execution of the function
		#commandline_insert("garden_api/test_deploiement_projet_territorial_uai.csv")
	