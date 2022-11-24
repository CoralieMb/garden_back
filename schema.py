from flask import current_app
from flask_marshmallow import Marshmallow
from garden_api.models import Marche, ProjetTerritorialUai, TitulaireMarche
from garden_api.models import Plateforme
from garden_api.models import Academie
from garden_api.models import Exploitant
from garden_api.models import Ministere
from garden_api.models import ProjetNational
from garden_api.models import TypeProjetTerritorial

ma = Marshmallow(current_app)

class TerritorialProjectSchema(ma.Schema):
    class Meta:
        fields = ("id_projet_territorial_uai", "lib_projet_territorial_uai_long", "lib_projet_territorial_uai_court", "id_type_projet_territorial")
        model = ProjetTerritorialUai

territorial_project_schema = TerritorialProjectSchema()
territorial_projects_schema = TerritorialProjectSchema(many=True)

class TerritorialProjectTypeSchema(ma.Schema):
    class Meta:
        fields = ("id_type_projet_territorial", "lib_type_projet_territorial")
        model = TypeProjetTerritorial

territorial_project_type_schema = TerritorialProjectTypeSchema()
territorial_projects_type_schema = TerritorialProjectTypeSchema(many=True)

class NationalProjectSchema(ma.Schema):
    class Meta:
        fields = ("id_projet_nat", "lib_projet_nat")
        model = ProjetNational

national_project_schema = NationalProjectSchema()
national_projects_schema = NationalProjectSchema(many=True)

class PlateformSchema(ma.Schema):
    class Meta:
        fields = ("id_plateforme", "lib_plateforme_long", "lib_plateforme_court", "id_editeur", "etat", "id_type_projet_territorial")
        model = Plateforme

plateform_schema = PlateformSchema()
plateforms_schema = PlateformSchema(many=True)

class AcademiaSchema(ma.Schema):
    class Meta:
        fields = ("id_academie", "lib_academie", "nouvel_id_academie", "id_region_academique")
        model = Academie

academia_schema = AcademiaSchema()
academias_schema = AcademiaSchema(many=True)

class ExploitantSchema(ma.Schema):
    class Meta:
        fields = ("id_exploitant", "lib_exploitant_long", "lib_exploitant_court", "role", "etat")
        model = Exploitant

exploitant_schema = ExploitantSchema()
exploitants_schema = ExploitantSchema(many=True)

class MinistrySchema(ma.Schema):
    class Meta:
        fields = ("id_ministere", "acronyme_ministere", "lib_ministere")
        model = Ministere

schema_ministry = MinistrySchema()
schema_ministries = MinistrySchema(many=True)

class OfficialMarketSchema(ma.Schema):
    class Meta:
        fields = ("id_titulaire_marche", "id_plateforme", "id_projet_territorial_uai", "id_exploitant", "id_marche")
        model = TitulaireMarche

schema_official_market = OfficialMarketSchema()
schema_official_markets = OfficialMarketSchema(many=True)

class MarketSchema(ma.Schema):
    class Meta:
        fields = ("id_marche", "lib_marche", "commentaire", "date_debut_marche", "date_fin_marche", "duree_maximale")
        model = Marche

schema_market = MarketSchema()
schema_markets = MarketSchema(many=True)