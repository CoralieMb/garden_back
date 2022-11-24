from flask import request
from flask_restful import Resource, fields, marshal as flask_marshall
from http import HTTPStatus
from garden_api.utils.rest_utils import entity_not_found_response
from garden_api.models import db, Marche as MarcheEntity
from sqlalchemy import func


class MarcheDTO(MarcheEntity):
    titulaires_marche = []

def marshal(entity: MarcheEntity):

    resource_fields = {
        "id": fields.Integer(attribute="id_marche"),
        "libelle": fields.String(attribute="lib_marche"),
        "commentaire": fields.String(attribute="commentaire"),
        "debut_marche": fields.DateTime(attribute="date_debut_marche"),
        "fin_marche": fields.DateTime(attribute="date_fin_marche"),
        "duree_maximale": fields.Integer(attribute="duree_maximale"),
        "plateforme": {
            "id": fields.Integer(attribute="titulaire_marche.id_plateforme"),
            "libelle": fields.String(attribute="plateforme.lib_plateforme_long")
        },
        "exploitant": {
            "id": fields.Integer(attribute="titulaire_marche.id_exploitant"),
            "libelle": fields.String(attribute="exploitant.lib_exploitant_long")
        },
        "projet_territorial": {
            "id": fields.Integer(attribute="titulaire_marche.id_projet_territorial_uai"),
            "libelle": fields.String(attribute="projet_territorial_uai.lib_projet_territorial_uai_court")
        }}
    return flask_marshall(entity, resource_fields)


def unmarshal(json):
    entity = MarcheEntity()
    entity.id_marche = json.get('id')
    entity.lib_marche = json.get('libelle')
    entity.commentaire = json.get('commentaire')
    entity.debut_marche = json.get('date_debut_marche')
    entity.fin_marche = json.get('date_fin_marche')
    entity.duree_maximale = json.get('duree_maximale')

    entity.id_plateforme = json.get(
        'plateforme', {}).get("id")
    entity.id_exploitant = json.get('exploitant', {}).get("id")
    entity.id_projet_territorial_uai = json.get(
        'projet_territorial', {}).get("id")
    return entity


class Market(Resource):

    # GET all the mache

    def get(self):
        try:
            from garden_api.models import db, Marche, TitulaireMarche, Plateforme, Exploitant, ProjetTerritorialUai

            response_data = []

            # global query

            # recuperer l'objet Marche
            # piur chaque Marche recuperer les lignes TitulaireMarche

            '''marche_request = db.session.query(Marche.lib_marche, Marche.date_debut_marche, Marche.date_fin_marche, Marche.duree_maximale, Marche.commentaire, func.group_concat(Plateforme.lib_plateforme_long.distinct()),
                                              func.group_concat(Exploitant.lib_exploitant_long.distinct()), func.group_concat(
                                                  ProjetTerritorialUai.lib_projet_territorial_uai_long.distinct()),
                                              Marche.id_marche, Exploitant.id_exploitant, Plateforme.id_plateforme, ProjetTerritorialUai.id_projet_territorial_uai)\
                .join(TitulaireMarche, TitulaireMarche.id_marche == Marche.id_marche)\
                .join(Plateforme, Plateforme.id_plateforme == TitulaireMarche.id_plateforme)\
                .join(Exploitant, Exploitant.id_exploitant == TitulaireMarche.id_exploitant)\
                .join(ProjetTerritorialUai, ProjetTerritorialUai.id_projet_territorial_uai == TitulaireMarche.id_projet_territorial_uai)\
                .group_by(Marche.lib_marche)\
                .order_by(asc(Marche.date_fin_marche), asc(Marche.date_debut_marche))'''
            marche_request = db.session.query(Marche)
            for marche_item in marche_request:
                marcheDTO = MarcheDTO()
                titulaires_query = db.session.query(Marche.lib_marche, Marche.date_debut_marche, Marche.date_fin_marche, Marche.duree_maximale, Marche.commentaire, func.group_concat(Plateforme.lib_plateforme_long.distinct()),
                                              func.group_concat(Exploitant.lib_exploitant_long.distinct()), func.group_concat(
                                                  ProjetTerritorialUai.lib_projet_territorial_uai_long.distinct()),
                                              Marche.id_marche, Exploitant.id_exploitant, Plateforme.id_plateforme, ProjetTerritorialUai.id_projet_territorial_uai)\
                .join(TitulaireMarche, TitulaireMarche.id_marche == Marche.id_marche)\
                .join(Plateforme, Plateforme.id_plateforme == TitulaireMarche.id_plateforme)\
                .join(Exploitant, Exploitant.id_exploitant == TitulaireMarche.id_exploitant)\
                .join(ProjetTerritorialUai, ProjetTerritorialUai.id_projet_territorial_uai == TitulaireMarche.id_projet_territorial_uai)\
                .group_by(Marche.lib_marche)\
                .order_by(asc(Marche.date_fin_marche), asc(Marche.date_debut_marche))
                marcheDTO.titulaires_marche = titulaires_query
                if marche_item._data[2] is not None:
                    end_date = marche_item._data[2].strftime("%Y-%m-%d")
                else:
                    end_date = marche_item._data[2]
                line = {
                    "lib_marche": marche_item._data[0],
                    "date_debut_marche": marche_item._data[1].strftime("%Y-%m-%d"),
                    "date_fin_marche": end_date,
                    "duree_maximale": marche_item._data[3],
                    "commentaire": marche_item._data[4],
                    "lib_plateforme_long": marche_item._data[5],
                    "lib_exploitant_long": marche_item._data[6],
                    "lib_projet_territorial_uai_long": marche_item._data[7],
                    "id_marche": marche_item._data[8],
                    "id_exploitant": marche_item._data[9],
                    "id_plateforme": marche_item._data[10],
                    "id_projet_territorial_uai": marche_item._data[11],
                }

                response_data.append(line)

            return jsonify(response_data)

        except Exception as e:
            print(e)

    # (POST) : add market

    def post(self):
        from garden_api.models import db, Marche, TitulaireMarche
        #from garden_api.schema import plateform_schema
        try:
            json = request.json
            lib_marche = json['lib_marche']
            id_projet_territorial_uai = json['id_projet_territorial_uai']
            date_debut_marche = json['date_debut_marche']
            date_fin_marche = json['date_fin_marche']
            duree_maximale = json['duree_maximale']
            id_exploitant = json["id_exploitant"]
            id_plateforme = json['id_plateforme']
            commentaire = json["commentaire"]

            # If the following values exist
            if lib_marche and date_debut_marche and duree_maximale and id_projet_territorial_uai and id_exploitant and id_plateforme and request.method == 'POST':
                # we check if the label already exists
                label_exists = db.session.query(Marche.lib_marche).filter(
                    func.lower(Marche.lib_marche) == lib_marche.lower()).first() is not None
                if label_exists:

                    #  if the labels exist we don't add the market.
                    return 'Le marché ' + lib_marche + ' existe déjà.', 'false'

                else:
                    # if the labels don't exist, we add the market
                    market_add = Marche(lib_marche=lib_marche, date_debut_marche=date_debut_marche,
                                        date_fin_marche=date_fin_marche, duree_maximale=duree_maximale, commentaire=commentaire)
                    db.session.add(market_add)
                    db.session.commit()

                    search_of_id_marche = db.session.query(
                        Marche).filter_by(lib_marche=lib_marche).all()

                    market_correspondance_add = TitulaireMarche(
                        id_marche=search_of_id_marche[0].id_marche, id_projet_territorial_uai=id_projet_territorial_uai, id_exploitant=id_exploitant, id_plateforme=id_plateforme)
                    db.session.add(market_correspondance_add)
                    db.session.commit()

                    return 'Le marché ' + lib_marche + ' a bien été ajouté', 'true'

                # return market_schema.dump(market_add)

            else:
                resp = jsonify('Il manque des données')
                resp.status_code = 500
                return resp

        except Exception as e:
            print(e)
            resp = jsonify('Echec de l\'ajout du marché')
            resp.status_code = 400

    # PUT : update market

    # id_marche, id_projet_territorial_uai, id_exploitant and id_plateforme = primary key of "titulaire_marche" table

    def put(self, id_marche, id_projet_territorial_uai, id_exploitant, id_plateforme):
        from garden_api.models import db, Marche, TitulaireMarche
        #from garden_api.schema import plateform_schema

        try:
            json = request.json
            lib_marche = json['lib_marche']
            id_projet_territorial_uai = json['id_projet_territorial_uai']
            date_debut_marche = json['date_debut_marche']
            date_fin_marche = json['date_fin_marche']
            duree_maximale = json['duree_maximale']
            id_exploitant = json["id_exploitant"]
            id_plateforme = json['id_plateforme']
            commentaire = json["commentaire"]

            # If the following values exist
            if lib_marche and date_debut_marche and duree_maximale and id_projet_territorial_uai and id_exploitant and id_plateforme and id_marche and request.method == 'PUT':
                # we get the row of the id_marche
                update_market = db.session.query(
                    Marche).filter_by(id_marche=id_marche).first()
                update_market_t = db.session.query(TitulaireMarche).filter_by(
                    id_marche=id_marche, id_projet_territorial_uai=id_projet_territorial_uai, id_exploitant=id_exploitant, id_plateforme=id_plateforme).first()

                # if we add a market end date, the market is over
                if date_fin_marche < date.today():
                    message = " est terminé."
                else:
                    message = " a bien été mobifié."

                # we update each element of the row
                update_market.lib_marche = lib_marche
                update_market.date_debut_marche = date_debut_marche
                update_market.date_fin_marche = date_fin_marche
                update_market.duree_maximale = duree_maximale
                update_market.commentaire = commentaire
                db.session.commit()

                update_market_t.id_projet_territorial_uai = id_projet_territorial_uai
                update_market_t.id_exploitant = id_exploitant
                update_market_t.id_plateforme = id_plateforme
                db.session.commit()
                return 'Le marché ' + lib_marche + message, 'true'

                # return plateform_schema.dump(update_market)

            else:
                resp = jsonify('Il manque des données')
                resp.status_code = 500
                return resp

        except Exception as e:
            print(e)
            resp = jsonify('Echec de la mise à jour du marché.')
            resp.status_code = 400
