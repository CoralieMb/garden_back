import os
from flask import Flask
from flask_restful import Api

# Import of all classes 

from .market.market import Market
from .market.market_nb import NbMarket
from .national_project.national_project import NationalProjects, NationalProject, NationalProjectCount
from .exploitant.exploitant import Exploitants, Exploitant, ExploitantCount
from garden_api.exploitant.exploitant_role import ExploitantRole
from .territorial_project.territorial_project import Projects, Project, AddProject, ProjectsCount
from .territorial_project_type.territorial_project_type import TerritorialProjectType, TerritorialProjectTypes, TerritorialProjectTypesCount
from .plateform.plateform import  Plateform, Plateforms, PlateformCount

from .db_config import close_db, get_db
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app*

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # MySQL configurations
        MYSQL_DATABASE_USER=os.environ.get('MYSQL_DATABASE_USER', 'root'),
        MYSQL_DATABASE_PASSWORD=os.environ.get('MYSQL_DATABASE_PASSWORD', ''),
        MYSQL_DATABASE_DB=os.environ.get('MYSQL_DATABASE_DB', 'referentiel_effios'),
        MYSQL_DATABASE_HOST=os.environ.get('MYSQL_DATABASE_HOST', 'localhost'),
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE','mysql://root@localhost/referentiel_effios'),
        SQLALCHEMY_ECHO = app.debug,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    app.teardown_appcontext(close_db)

    api = Api(app)

    # All routes

    # National project
    api.add_resource(NationalProjects, '/projets_nationaux')
    api.add_resource(NationalProject, '/projets_nationaux/<int:id_projet_nat>')
    api.add_resource(NationalProjectCount, '/projets_nationaux/nombre')

    # Plateform
    api.add_resource(Plateforms, '/plateformes')
    api.add_resource(Plateform,'/plateformes/<int:id_plateforme>')
    api.add_resource(PlateformCount, '/plateformes/nombre')

    # Market
    api.add_resource(Market, '/marche/', '/marche/<int:id_marche>/<int:id_projet_territorial_uai>/<int:id_exploitant>/<int:id_plateforme>')
    api.add_resource(NbMarket, '/marche/nombre/')

    # Territorial Project Type
    api.add_resource(TerritorialProjectType, '/types_projet_territoriaux/<int:id_type_projet_territorial>')
    api.add_resource(TerritorialProjectTypes, '/types_projet_territoriaux')
    api.add_resource(TerritorialProjectTypesCount, '/types_projet_territoriaux/nombre') 

    # Exploitant routes
    api.add_resource(Exploitants, '/exploitants')
    api.add_resource(Exploitant, '/exploitants/<int:id_exploitant>')
    api.add_resource(ExploitantCount, '/exploitants/nombre')
    api.add_resource(ExploitantRole, '/exploitants/role')

    # Project routes

    # All projects (get one project, edit one project and add one project)
    api.add_resource(Project, '/projets/<int:id_projet_territorial_uai>')
    api.add_resource(AddProject, '/projets')
    # Get all projects according the project type given in parameter 
    api.add_resource(Projects, '/projets/<string:lib_type_projet_territorial>')
    # Count all projects according the project type given in parameter 
    api.add_resource(ProjectsCount, '/projets/<string:lib_type_projet_territorial>/nombre')
   

    # Create an instance of CORS
    Cors = CORS(app)
    CORS(app, resources={r'/*': {'origins': '*'}}, CORS_SUPPORTS_CREDENTIALS=True)
    app.config['CORS_HEADERS'] = 'Content-Type'


    return app
