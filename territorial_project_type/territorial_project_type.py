from flask_restful import Resource, fields, marshal as flask_marshall
from http import HTTPStatus
from garden_api.utils.rest_utils import entity_not_found_response
from flask import jsonify, request
from garden_api.models import db, TypeProjetTerritorial as TypeProjetTerritorialEntity
from sqlalchemy import func


def marshal(entity: TypeProjetTerritorialEntity):
    resource_fields = {
        "id": fields.Integer(attribute="id_type_projet_territorial"),
        "libelle": fields.String(attribute="lib_type_projet_territorial")}
    return flask_marshall(entity, resource_fields)


def unmarshal(json):
    entity = TypeProjetTerritorialEntity()
    entity.id_type_projet_territorial = json.get('id')
    entity.lib_type_projet_territorial = json.get('libelle')
    return entity


def validate_save(territorial_project_type: TypeProjetTerritorialEntity):
    # common save validations for add and update
    # not common save validations must be performed in post() and put() functions
    if not territorial_project_type.lib_type_projet_territorial:
        return "Libélle obligatoire"
    return None


class TerritorialProjectType(Resource):
    def get(self, id_type_projet_territorial):
        territorial_project_type = db.session.get(
            TypeProjetTerritorialEntity, id_type_projet_territorial)
        if (territorial_project_type is None):
            return entity_not_found_response(id_type_projet_territorial)
        else:
            return marshal(territorial_project_type)

    # PUT : update

    def put(self, id_type_projet_territorial):
        try:
            territorial_project_type = unmarshal(request.json)

            if id_type_projet_territorial != territorial_project_type.id_type_projet_territorial:
                return "ids in url and body not matching", HTTPStatus.BAD_REQUEST

            validation_error = validate_save(territorial_project_type)
            if validation_error is not None:
                return validation_error, HTTPStatus.BAD_REQUEST

            # verifier qu'aucun type de projet existe avec le meme lib
            territorial_project_type_existante = db.session.query(TypeProjetTerritorialEntity).filter(
                (TypeProjetTerritorialEntity.id_type_projet_territorial != territorial_project_type.id_type_projet_territorial) &
                (func.lower(TypeProjetTerritorialEntity.lib_type_projet_territorial) == func.lower(territorial_project_type.lib_type_projet_territorial))).first()

            if territorial_project_type_existante:
                # if territorial project type short or long name exists return error
                msg = 'Le type de projet territorial existe déjà'
                return msg, HTTPStatus.BAD_REQUEST

            territorial_project_type_to_update = db.session.get(
                TypeProjetTerritorialEntity, id_type_projet_territorial)
            if territorial_project_type_to_update is None:
                return entity_not_found_response(id_type_projet_territorial)
            else:
                for column in TypeProjetTerritorialEntity.__table__.columns:
                    setattr(territorial_project_type_to_update, column.key,
                            getattr(territorial_project_type, column.key))
                db.session.commit()
                return marshal(territorial_project_type_to_update)
            
        except Exception as e:
            print(e)
            return 'Echec de la mise à jour', HTTPStatus.INTERNAL_SERVER_ERROR

class TerritorialProjectTypes(Resource):
     #GET all the territorial project types
	def get(self):
		try:
			territorial_project_type_request = db.session.query(TypeProjetTerritorialEntity)
			response_data = []
			for territorial_project_type_item in territorial_project_type_request:
				response_data.append(marshal(territorial_project_type_item))
			return response_data

		except Exception as e:
			print(e)
			return None, HTTPStatus.INTERNAL_SERVER_ERROR


 # (POST) : add territorial project type
	def post(self):
		try:
			territorial_project_type = unmarshal(request.json)
			
			validation_error = validate_save(territorial_project_type)
			if validation_error:
				return validation_error, HTTPStatus.BAD_REQUEST

			# we check if the label already exists
			territorial_project_type_existante = db.session.query(TypeProjetTerritorialEntity).filter(
				(func.lower(TypeProjetTerritorialEntity.lib_type_projet_territorial)==func.lower(territorial_project_type.lib_type_projet_territorial))).first()

			if territorial_project_type_existante:
				msg = 'Le type de projet territorial existe déjà'
				return msg, HTTPStatus.BAD_REQUEST					
			else:
				db.session.add(territorial_project_type)
				db.session.commit()
				return marshal(territorial_project_type)
		except Exception as e:
			print(e)
			return 'Echec de l\'ajout du type de projet territorial', HTTPStatus.INTERNAL_SERVER_ERROR


class TerritorialProjectTypesCount(Resource):
    def get(self):
        return db.session.query(TypeProjetTerritorialEntity.id_type_projet_territorial).count()