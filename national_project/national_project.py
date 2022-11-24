from flask import request
from flask_restful import Resource, fields, marshal as flask_marshall
from garden_api.models import db, ProjetNational as NationalProjectEntity
from http import HTTPStatus
from garden_api.utils.rest_utils import entity_not_found_response

def marshal(project):
    resource_fields = {
    "id": fields.Integer(attribute="id_projet_nat"),
    "libelle": fields.String(attribute="lib_projet_nat")
    }
    return flask_marshall(project, resource_fields)

def unmarshal(json):
    project = NationalProjectEntity()
    project.id_projet_nat = json.get('id')
    project.lib_projet_nat = json.get('libelle')
    return project

def validate_save(project:NationalProjectEntity):
	# common save validations for add and update
	# not common save validations must be performed in post() and put() functions
    if not project.lib_projet_nat:
        return "Libelle est obligatoire"
    return None

class NationalProject(Resource):
    # GET national project
    def get(self, id_projet_nat):
        nat_project = db.session.get(NationalProjectEntity, id_projet_nat)
        if (nat_project is None):
            return entity_not_found_response(id_projet_nat)
        else:
            return marshal(nat_project)

    # update national project
    def put(self, id_projet_nat):
        try:
            project = unmarshal(request.json)

            if id_projet_nat != project.id_projet_nat:
                return "ids in url and body not matching", HTTPStatus.BAD_REQUEST

            validation_error = validate_save(project)
            if validation_error:
                return validation_error, HTTPStatus.BAD_REQUEST

            update_national_project = db.session.get(NationalProjectEntity, id_projet_nat)
            if update_national_project is None:
                return entity_not_found_response(id_projet_nat)

            for column in NationalProjectEntity.__table__.columns:
                setattr(update_national_project, column.key, getattr(project, column.key))
            db.session.commit()
            return marshal(update_national_project)

        except Exception as e:
            print(e)
            return 'Echec de la mise à jour du projet national.', HTTPStatus.BAD_REQUEST

class NationalProjects(Resource):

    # GET all national projects
    def get(self, **kwargs):
        try:
            # GET all items
            response_data = []
            national_project_request = db.session.query(NationalProjectEntity)
            for national_project in national_project_request:
                response_data.append(
                    marshal(national_project))
            return response_data
        except Exception as e:
            print(e)
            return None, HTTPStatus.INTERNAL_SERVER_ERROR

    # add new national project
    def post(self):
        try:
            project = unmarshal(request.json)

            validation_error = validate_save(project)
            if validation_error:
                return validation_error, HTTPStatus.BAD_REQUEST

            db.session.add(project)
            db.session.commit()
            return marshal(project)

        except Exception as e:
            print(e)
            return 'Echec de l\'ajout du projet national', HTTPStatus.INTERNAL_SERVER_ERROR

class NationalProjectCount(Resource):
    # GET national projects count
    def get(self):
        return db.session.query(NationalProjectEntity.id_projet_nat).count()