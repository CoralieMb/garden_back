import unittest
import xmlrunner
import flask_unittest
from garden_api import create_app
from test_unitaire.territorial_project_test import TerritorialProjectTest
from test_unitaire.plateforme_test import PlateformTest
from test_unitaire.market_test import MarketTest
from test_unitaire.national_project_test import NationalProjectTest
from test_unitaire.territorial_project_type_test import TerritorialProjectTypeTest
from test_unitaire.exploitant_test import ExploitantTest

suite = flask_unittest.LiveTestSuite(create_app({'SQLALCHEMY_TRACK_MODIFICATIONS': False,
                                                 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'}))
suite.addTest(unittest.makeSuite(TerritorialProjectTest))
suite.addTest(unittest.makeSuite(MarketTest))
suite.addTest(unittest.makeSuite(NationalProjectTest))
suite.addTest(unittest.makeSuite(TerritorialProjectTypeTest))
suite.addTest(unittest.makeSuite(PlateformTest))
suite.addTest(unittest.makeSuite(ExploitantTest))

xmlrunner.XMLTestRunner().run(suite)
