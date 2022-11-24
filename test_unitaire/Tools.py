from garden_api import create_app
import unittest
import garden_api.models
import datetime


class TestGeneric(unittest.TestCase):

    # Method setUp and TearDown : https://docs.python.org/3/library/unittest.html

    # setUp() is called before each test. Here, we use it to reset test environment (ex : if we test the route to add a projet ent, setUp will recreate the original sql file)
    # unitest.sqlite is our sql file (= referentiel_effios.sql) and sql_backup is a copy of the original sql file (unitest.sqlite) that we keep and reuse for each test
    # By using client.get we can send an HTTP GET request to the application with the given path
    def setUp(self):
        self.app = create_app({'SQLALCHEMY_TRACK_MODIFICATIONS': False,
                               'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', 'echo': "debug"})
        self.db = garden_api.models.db
        self.db.init_app(self.app)
        self.db.get_app = lambda item=None: self.app
        with self.app.app_context():
            self.db.drop_all(app=self.app)
            self.db.create_all(app=self.app)
            self.add_ministry()
            self.add_town()
            self.add_academia()
            self.add_uais()
            self.add_exploitants()
            self.add_plateforms()
            self.add_territorial_projects()
            self.add_deployements()
            self.add_market()
            self.add_national_project()
            self.add_territorial_project_type()
            self.add_official_market()

    # tearDown() is called after each test only if setUP() succeeded. Here, the method retake the copy of original sql file (sql_backup)
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all(app=self.app)

    def add_academia(self):
        from garden_api.models import Academie

        for item in ((0, 'Etranger', None, None),
                     (1, 'Paris', None, 8),
                     (2, 'Aix-Marseille', None, 17),
                     (3, 'Besançon', None, 9),
                     (4, 'Bordeaux', None, 14),
                     (5, 'Caen', None, 11),
                     (6, 'Clermont-Ferrand', None, 15),
                     (7, 'Dijon', None, 9),
                     (8, 'Grenoble', None, 15),
                     (9, 'Lille', None, 6),
                     (10, 'Lyon', None, 15)):
            self.db.session.add(Academie(id_academie=item[0], lib_academie=item[1],
                                         nouvel_id_academie=item[2], id_region_academique=item[3]))
        self.db.session.commit()

    def add_ministry(self):
        from garden_api.models import Ministere
        for item in ((0, 'ST', 'sans tutelle'),
                     (1, 'MEAE', 'ministère de europe et des affaires étrangères'),
                     (2, 'MC', 'ministère de la culture'),
                     (3, 'MAA', 'ministère de agriculture et de alimentation'),
                     (4, 'MA', 'ministère des Armées'),
                     (5, 'MEFR', 'ministère de l économie, des finances et de la relance'),
                     (6, 'MENJS', 'ministère de éducation nationale, de la jeunesse et des sports'),
                     (9, 'MI', 'ministère de intérieur'),
                     (10, 'MJ', 'ministère de la justice')):
            self.db.session.add(Ministere(id_ministere=item[0], acronyme_ministere=item[1], lib_ministere=item[2]))

        self.db.session.commit()

    def add_town(self):
        from garden_api.models import Commune

        for item in (('01004', '84', '01', 'Ambérieu-en-Bugey', '01500'),
                     ('01025', '84', '01', 'Bâgé-Dommartin', '01380'),
                     ('01033', '84', '01', 'Valserhône', '01200'),
                     ('01034', '84', '01', 'Belley', '01306'),
                     ('01053', '84', '01', 'Bourg-en-Bresse', '01011')):
            self.db.session.add(
                Commune(code_commune=item[0], code_region=item[1], code_departement=item[2], lib_commune=item[3],
                        code_postal=item[4]))
        self.db.session.commit()

    def add_exploitants(self):
        from garden_api.models import Exploitant

        for item in ((1, 'Ac_Rennes', 'Ac_Rennes', 0, 1),
                     (2, 'Gip_Recia', 'Gip_Recia', 0, 1),
                     (3, 'Itop_Education', 'Itop_Education', 0, 1),
                     (4, 'itslearning', 'itslearning', 0, 1),
                     (5, 'Kosmos', 'Kosmos', 0, 1),
                     (6, 'Men_Pcll', 'Men_Pcll', 0, 1),
                     (7, 'Metropole_Lyon', 'Metropole_Lyon', 0, 1),
                     (8, 'Ode', 'Ode', 0, 1),
                     (9, 'Beneylu', 'Beneylu', 0, 1),
                     (10, 'Cgi', 'Cgi', 0, 1)):
            self.db.session.add(Exploitant(id_exploitant=item[0], lib_exploitant_long=item[1],
                                           lib_exploitant_court=item[2], role=item[3], etat=item[4]))
        self.db.session.commit()

    def add_plateforms(self):
        from garden_api.models import Plateforme

        for item in ((1, 'Ent.recia', 'Ent.recia', 2, 1, 1),
                     (2, 'Envole', 'Envole', 6, 1, 1),
                     (3, 'Itslearning', 'Itslearning', 4, 1, 1),
                     (4, 'Laclasse.com', 'Laclasse.com', 7, 1, 1),
                     (5, 'Open_ent_ng/one/neo', 'Open_ent_ng/one/neo', 8, 1, 1),
                     (6, 'Oze', 'Oze', 3, 1, 1),
                     (7, 'Oze_1D', 'Oze_1D', 3, 1, 1),
                     (8, 'Skolengo', 'Skolengo', 5, 1, 1),
                     (9, 'Toutatice', 'Toutatice', 1, 1, 1),
                     (10, 'Beneylu School', 'Beneylu School', 9, 1, 1)):
            self.db.session.add(Plateforme(id_plateforme=item[0], lib_plateforme_long=item[1],
                                           lib_plateforme_court=item[2], id_editeur=item[3], etat=item[4],
                                           id_type_projet_territorial=item[5]))
        self.db.session.commit()

    def add_uais(self):
        from garden_api.models import Uai
        for item in (('0010001W', 'Auvergne-Rhône-Alpes', 3, 'ALEXANDRE BERARD', 320, 10, '01004', 'Ouvert', 6, "NULL",
                      '', 'PU', "NULL", 'LP LYC METIER'),
                     ('0010002X', 'Ain', 2, 'SAINT-EXUPERY', 340, 10, '01004', 'Ouvert', 6, 1, 'BP508', 'PU', "NULL",
                      'CLG'),
                     ('0010005A', 'Ain', 2, 'ROGER POULNARD', 340, 10, '01025', 'Ouvert', 6, 1, 'BP11', 'PU', "NULL",
                      'CLG'),
                     ('0010006B', 'Auvergne-Rhône-Alpes', 3, 'SAINT-EXUPERY', 306, 10, '01033', 'Ouvert', 6, "NULL",
                      'BP616', 'PU', '101', 'LPO LYC METIER'),
                     ('0010007C', 'Auvergne-Rhône-Alpes', 3, 'BRILLAT SAVARIN', 320, 10, '01033', 'Fermé', 6, "NULL",
                      'BP616', 'PU', '101', 'LP'),
                     ('0010008D', 'Ain', 2, 'SAINT-EXUPERY', 340, 10, '01033', 'Ouvert', 6, 1, 'BP616', 'PU', '101',
                      'CLG'),
                     ('0010010F', 'Auvergne-Rhône-Alpes', 3, 'DU BUGEY', 300, 10, '01034', 'Ouvert', 6, "NULL", 'BP157',
                      'PU', '102', 'LGT'),
                     ('0010013J', 'Auvergne-Rhône-Alpes', 3, 'LALANDE', 302, 10, '01053', 'Ouvert', 6, "NULL", 'BP301',
                      'PU', "NULL", 'LG'),
                     ('0010014K', 'Auvergne-Rhône-Alpes', 3, 'EDGAR QUINET', 300, 10, '01053', 'Ouvert', 6, "NULL",
                      'BP302', 'PU', "NULL", 'LGT'),
                     ('0010016M', 'Auvergne-Rhône-Alpes', 3, 'JOSEPH-MARIE CARRIAT', 306, 10, '01053', 'Ouvert', 6,
                      "NULL", 'BP60309', 'PU', '104', 'LPO'),
                     ('0010017N', 'Auvergne-Rhône-Alpes', 3, 'LPO JOSEPH-MARIE CARRIAT', 334, 10, '01053', 'Ouvert', 6,
                      "NULL", 'BP60309', 'PU', '104', 'SEP'),
                     ('0010018P', 'Ain', 2, 'DU REVERMONT', 340, 10, '01053', 'Ouvert', 6, 1, '', 'PU', "NULL", 'CLG')):
            self.db.session.add(Uai(uai=item[0], collectivite=item[1], id_type_collectivite=item[2],
                                    patronyme=item[3], code_nature=item[4],
                                    code_academie=item[5], code_commune=item[6], etat_etablissement=item[7],
                                    id_ministere=item[8], id_circonscription=item[9], boite_postale=item[10],
                                    secteur=item[11], zone_cite_scolaire=item[12], sigle_uai=item[13]))
        self.db.session.commit()

    def add_territorial_projects(self):
        from garden_api.models import ProjetTerritorialUai
        for item in ((1, '@Ucollege84', '@Ucollege84', 1, 0),
                     (2, 'AGORA06', 'AGORA06', 1, 0),
                     (3, 'Arsène76', 'Arsène76', 1, 0),
                     (4, 'Chercan', 'Chercan', 1, 0),
                     (5, 'Colibri', 'Colibri', 1, 0),
                     (6, 'College_Eureliens', 'College_Eureliens', 1, 0),
                     (7, 'Colleges41', 'Colleges41', 1, 0),
                     (8, 'Cybercollège', 'Cybercollège', 1, 0),
                     (9, 'Eclat-BFC', 'Eclat-BFC', 1, 0),
                     (10, 'eCollège Yvelines', 'eCollège Yvelines', 1, 0),
                     (50, 'Ent_Var_Toulon', 'Ent_Var_Toulon', 1, 0)):
            self.db.session.add(
                ProjetTerritorialUai(id_projet_territorial_uai=item[0], lib_projet_territorial_uai_long=item[1],
                                     lib_projet_territorial_uai_court=item[2],
                                     id_type_projet_territorial=item[3],
                                     etat=item[4]))
        self.db.session.commit()

    def add_deployements(self):
        from garden_api.models import DeploiementProjetTerritorialUai
        for item in ((1, '0220003J', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (2, '0220006M', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (3, '0220008P', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (4, '0220009R', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (5, '0220013V', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (6, '0220015X', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (7, '0220018A', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (8, '0220019B', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (9, '0220023F', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (10, '0220027K', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (11, '0220029M', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (12, '0220032R', 40, 9, '01/01/2013', "NULL", "NULL"),
                     (13, '0220038X', 40, 9, '01/01/2013', "NULL", "NULL")):
            self.db.session.add(
                DeploiementProjetTerritorialUai(id_deploiement_projet_territorial_uai=item[0], uai=item[1],
                                                id_projet_territorial_uai=item[2], id_plateforme=item[3],
                                                date_debut=item[4], date_fin=item[5], commentaire=item[6]))
        self.db.session.commit()

    def add_market(self):
        from garden_api.models import Marche

        for item in ((1,
                      'Fourniture D\'Un Espace Numérique De Travail (Ent) Pour Les Collèges Du Var Et Les écoles Primaires De Toulon',
                      'Groupement de commandes constitué par le Département du Var et la Mairie de Toulon. Critères d\'attribution : Valeur technique (45%)  Prix (55%). Durée de 2 ans renouvelable 4 fois par période d\'1 an. Montants : Département du VAR : Total année 1 et 2 : mini 100k€ maxi 500k€. Autres années : mini 20 k€ maxi 250 k€. Ville de Toulon : Total année 1 et 2 : mini 40k€ maxi 160k€. Autres années : mini 20 k€ maxi 80 k€. BOAMP : https://www.boamp.fr/avis/detail/22-39753?xtor=EPR-2',
                      datetime.date.fromisoformat('2022-04-13'), None, 72),):
            self.db.session.add(Marche(id_marche=item[0], lib_marche=item[1],
                                       commentaire=item[2], date_debut_marche=item[3], date_fin_marche=item[4],
                                       duree_maximale=item[5]))
        self.db.session.commit()

    def add_national_project(self):
        from garden_api.models import ProjetNational

        for item in ((1, 'DNMA'),
                     (2, 'GAR')):
            self.db.session.add(ProjetNational(id_projet_nat=item[0], lib_projet_nat=item[1]))
        self.db.session.commit()

    def add_territorial_project_type(self):
        from garden_api.models import TypeProjetTerritorial

        for item in ((1, 'PROJET_ENT'),
                     (2, 'RD_MEN')):
            self.db.session.add(
                TypeProjetTerritorial(id_type_projet_territorial=item[0], lib_type_projet_territorial=item[1]))
        self.db.session.commit()

    def add_official_market(self):
        from garden_api.models import TitulaireMarche

        for item in ((1, 5, 50, 8, 1),
                     (2, 5, 50, 10, 1)):
            self.db.session.add(
                TitulaireMarche(id_titulaire_marche=item[0], id_plateforme=item[1], id_projet_territorial_uai=item[2],
                                id_exploitant=item[3], id_marche=item[4]))
        self.db.session.commit()
