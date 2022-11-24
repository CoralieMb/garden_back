from flask_restful import Resource, fields, marshal as flask_marshall
from flask import  request
from sqlalchemy import desc, func
from http import HTTPStatus
from garden_api.utils.rest_utils import entity_not_found_response
from garden_api.models import db, ProjetTerritorialUai as ProjetTerritorialUaiEntity, TypeProjetTerritorial as TypeProjetTerritorialEntity


def marshal(entity: ProjetTerritorialUaiEntity):
    resource_fields = {
        "id": fields.Integer(attribute="id_projet_territorial_uai"),
        "libelle_long": fields.String(attribute="lib_projet_territorial_uai_long"),
        "libelle_court": fields.String(attribute="lib_projet_territorial_uai_court"),
        "etat": fields.Integer,
        "id_type_projet_territorial": fields.Integer(attribute="id_type_projet_territorial")}
    return flask_marshall(entity, resource_fields)


def unmarshal(json):
    entity = ProjetTerritorialUaiEntity()
    entity.id_projet_territorial_uai = json.get('id')
    entity.lib_projet_territorial_uai_long = json.get('libelle_long')
    entity.lib_projet_territorial_uai_court = json.get('libelle_court')
    entity.etat = json.get('etat')
    entity.id_type_projet_territorial = json.get('id_type_projet_territorial')
    return entity


def validate_save(project: ProjetTerritorialUaiEntity):
    # common save validations for add and update
    # not common save validations must be performed in post() and put() functions
    if not project.lib_projet_territorial_uai_long:
        return "Libélle long obligatoire"

    if not project.lib_projet_territorial_uai_court:
        return "Libelle court est obligatoire"

    return None


class Project(Resource):
    # get on project (ent or rdmen)

    def get(self, id_projet_territorial_uai):
        project = db.session.get(
            ProjetTerritorialUaiEntity, id_projet_territorial_uai)
        if project is None:
            return entity_not_found_response(id_projet_territorial_uai)
        else:
            return marshal(project)

     # PUT : update ent project

    def put(self, id_projet_territorial_uai):
        try:
            project = unmarshal(request.json)
            if id_projet_territorial_uai != project.id_projet_territorial_uai:
                return "ids in url and body not matching", HTTPStatus.BAD_REQUEST

            validation_error = validate_save(project)
            if validation_error is not None:
                return validation_error, HTTPStatus.BAD_REQUEST

            # vérifier qu'aucun projet ent existe avec le meme lib court & long
            project_existante = db.session.query(ProjetTerritorialUaiEntity).filter(
                (ProjetTerritorialUaiEntity.id_projet_territorial_uai != project.id_projet_territorial_uai) &
                ((func.lower(ProjetTerritorialUaiEntity.lib_projet_territorial_uai_long) == func.lower(project.lib_projet_territorial_uai_long)) |
                 (func.lower(ProjetTerritorialUaiEntity.lib_projet_territorial_uai_court) == func.lower(project.lib_projet_territorial_uai_court)))).first()

            if project_existante:
                # if project short or long name exists return error
                msg = 'Le projet ent existe déjà à l\'état ' + \
                    ('Actif' if (project_existante.etat == 1) else (
                        'Inactif' if (project_existante.etat == 0) else ''))
                return msg, HTTPStatus.BAD_REQUEST

            project_to_update = db.session.get(
                ProjetTerritorialUaiEntity, id_projet_territorial_uai)
            if project_to_update is None:
                return entity_not_found_response(id_projet_territorial_uai)
            else:
                for column in ProjetTerritorialUaiEntity.__table__.columns:
                    setattr(project_to_update, column.key,
                            getattr(project, column.key))
                db.session.commit()
                return marshal(project_to_update)
        except Exception as e:
            print(e)
            return 'Echec de la mise à jour', HTTPStatus.INTERNAL_SERVER_ERROR


class Projects(Resource):

    # GET all the projects acccording the project type asked
    def get(self, lib_type_projet_territorial):
        try:
            # we get the id of the project type thank to the project type lib given in parameter
            type_projet_territorial = db.session.query(TypeProjetTerritorialEntity).filter(
                TypeProjetTerritorialEntity.lib_type_projet_territorial == lib_type_projet_territorial).first()
            id_type_projet_territorial_found = type_projet_territorial.id_type_projet_territorial

            ent_project_request = db.session.query(
                ProjetTerritorialUaiEntity).filter_by(id_type_projet_territorial=id_type_projet_territorial_found)
            response_data = []
            for ent_project_item in ent_project_request:
                response_data.append(marshal(ent_project_item))
            return response_data

        except Exception as e:  # Exception = all native exceptions which do not get out of the systeme
            print(e)
            return None, HTTPStatus.INTERNAL_SERVER_ERROR


class AddProject(Resource):
    # (POST) : add project
    def post(self):
        try:
            project = unmarshal(request.json)
            
            validation_error = validate_save(project)
            if validation_error:
                return validation_error, HTTPStatus.BAD_REQUEST
            if project.etat != 1:  # The ent project must be active to the creation
                project.etat = 1

            # we check if the long or short label already exists
            project_existance = db.session.query(ProjetTerritorialUaiEntity).filter(
                (func.lower(ProjetTerritorialUaiEntity.lib_projet_territorial_uai_long) == func.lower(project.lib_projet_territorial_uai_long)) |
                (func.lower(ProjetTerritorialUaiEntity.lib_projet_territorial_uai_court) == func.lower(project.lib_projet_territorial_uai_court))).first()

            if project_existance:
                # if ent project short or long name exists return error
                msg = 'Le projet ent existe déjà à l\'état ' + \
                    ('Actif' if (project_existance.etat == 1) else (
                        'Inactif' if (project_existance.etat == 0) else ''))
                return msg, HTTPStatus.BAD_REQUEST
            else:
                db.session.add(project)
                db.session.commit()
                return marshal(project)

        except Exception as e:
            print(e)
            return 'Echec de l\'ajout du projet ent', HTTPStatus.INTERNAL_SERVER_ERROR


class ProjectsCount(Resource):

    # GET the number of projets according project type given in parameter
    def get(self, lib_type_projet_territorial):
        # we get the id of the project type thank to the project type lib given in parameter
        type_projet_territorial = db.session.query(TypeProjetTerritorialEntity).filter(
            TypeProjetTerritorialEntity.lib_type_projet_territorial == lib_type_projet_territorial).first()
        id_type_projet_territorial_found = type_projet_territorial.id_type_projet_territorial
        
        return db.session.query(ProjetTerritorialUaiEntity.id_type_projet_territorial).filter_by(id_type_projet_territorial=id_type_projet_territorial_found).count()
