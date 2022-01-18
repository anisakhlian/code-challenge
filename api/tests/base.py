import unittest

from models import db_session
from unittest import mock
from models.pg_helpers.sqlalchemy_helper import SqlalchemyHelper

class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from app import app
        app.testing = True
        cls.app = app.test_client()
        cls._app = app

    def setUp(self):
        self.connection = SqlalchemyHelper.connection
        self.trans = self.connection.begin()
        self.session = db_session

    def tearDown(self):
        self.session.remove()
        self.trans.rollback()
