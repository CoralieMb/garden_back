from flask import request
from flask_restful import Resource, fields, marshal as flask_marshall
from http import HTTPStatus
from garden_api.utils.rest_utils import entity_not_found_response
from garden_api.models import db, Plateforme as PlateformEntity
from sqlalchemy import func

def marshal(entity:PlateformEntity):
	resource_fields = {
    "id": fields.Integer(attribute="id_plateforme"),
	"libelle_long": fields.String(attribute="lib_plateforme_long"),
	"libelle_court": fields.String(attribute="lib_plateforme_court"),
	"etat":fields.Integer,
	"editeur" : {
		"id" : fields.Integer(attribute="id_editeur"),
		"libelle_long" : fields.String(attribute="exploitant.lib_exploitant_long")
	},
	"type_projet_territorial" : {
		"id": fields.Integer(attribute="id_type_projet_territorial"),
		"libelle":fields.String(attribute="type_projet_territorial.lib_type_projet_territorial")
	}}
	return flask_marshall(entity, resource_fields)

def unmarshal(json):
	entity = PlateformEntity()
	entity.id_plateforme = json.get('id')
	entity.lib_plateforme_long = json.get('libelle_long')
	entity.lib_plateforme_court = json.get('libelle_court')
	entity.etat = json.get('etat')
	entity.id_type_projet_territorial = json.get('type_projet_territorial', {}).get("id")
	entity.id_editeur = json.get('editeur', {}).get("id")
	return entity

def validate_save(platform:PlateformEntity):
	# common save validations for add and update
	# not common save validations must be performed in post() and put() functions
	if not platform.lib_plateforme_long:
		return "Libélle long obligatoire"

	if not platform.lib_plateforme_court:
		return "Libelle court est obligatoire"

	if not platform.id_editeur:
		return "L'éditeur est obligatoire"

	if not platform.id_type_projet_territorial:
		return "Le type du projet territorial est obligatoire"

	return None

class Plateform(Resource):
	def get(self, id_plateforme):
		platform = db.session.get(PlateformEntity, id_plateforme)
		if (platform is None):
			return entity_not_found_response(id_plateforme)
		else:
			return marshal(platform)

	# PUT : update plateform 
	def put(self, id_plateforme):
		try:
			platform = unmarshal(request.json)

			if id_plateforme != platform.id_plateforme:
				return "ids in url and body not matching", HTTPStatus.BAD_REQUEST

			validation_error = validate_save(platform)
			if validation_error is not None:
				return validation_error, HTTPStatus.BAD_REQUEST

			# verifier qu'aucune plateforme existe avec le meme lib court & long
			platform_existante = db.session.query(PlateformEntity).filter(
				(PlateformEntity.id_plateforme != platform.id_plateforme) &
				((func.lower(PlateformEntity.lib_plateforme_long)==func.lower(platform.lib_plateforme_long)) |
				(func.lower(PlateformEntity.lib_plateforme_court)==func.lower(platform.lib_plateforme_court)))).first()

			if platform_existante:
				# if platform short or long name exists return error
				msg = 'La plateforme existe déjà à l\'état ' + ('Actif' if (platform_existante.etat == 1) else ('Inactif' if (platform_existante.etat == 0) else ''))
				return msg, HTTPStatus.BAD_REQUEST	

			platform_to_update = db.session.get(PlateformEntity, id_plateforme)
			if platform_to_update is None:
				return entity_not_found_response(id_plateforme)
			else:
				for column in PlateformEntity.__table__.columns:
					setattr(platform_to_update, column.key, getattr(platform, column.key))
				db.session.commit()
				return marshal(platform_to_update)
		except Exception as e:
			print(e)
			return 'Echec de la mise à jour', HTTPStatus.INTERNAL_SERVER_ERROR

class Plateforms(Resource):
    #GET all the plateforms
	def get(self):
		try:
			plateform_request = db.session.query(PlateformEntity)
			response_data = []
			for plateform_item in plateform_request:
				response_data.append(marshal(plateform_item))
			return response_data

		except Exception as e:
			print(e)
			return None, HTTPStatus.INTERNAL_SERVER_ERROR

	# (POST) : add plateform
	def post(self):
		try:
			platform = unmarshal(request.json)
			
			validation_error = validate_save(platform)
			if validation_error:
				return validation_error, HTTPStatus.BAD_REQUEST

			if platform.etat != 1:
				platform.etat = 1 #La plateforme doit etre active à la création

			# we check if the long or short label already exists
			platform_existante = db.session.query(PlateformEntity).filter(
				(func.lower(PlateformEntity.lib_plateforme_long)==func.lower(platform.lib_plateforme_long)) |
				(func.lower(PlateformEntity.lib_plateforme_court)==func.lower(platform.lib_plateforme_court))).first()

			if platform_existante:
				# if platform short or long name exists return error
				msg = 'La plateforme existe déjà à l\'état ' + ('Actif' if (platform_existante.etat == 1) else ('Inactif' if (platform_existante.etat == 0) else ''))
				return msg, HTTPStatus.BAD_REQUEST					
			else:
				db.session.add(platform)
				db.session.commit()
				return marshal(platform)
		except Exception as e:
			print(e)
			return 'Echec de l\'ajout de la plateforme', HTTPStatus.INTERNAL_SERVER_ERROR

class PlateformCount(Resource):
    def get(self):
        return db.session.query(PlateformEntity.id_plateforme).count()