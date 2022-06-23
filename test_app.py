import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from settings import *
from models import *
from app import app

class CastingTestCast(unittest.TestCase):

    def setup(self):
        '''Define test variable and initialize the test app'''
        self.app = app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)


        with self.app.app_context():
            self.db = SQLAlchemy
            self.db.init_app(self.app)
            self.db.create_all()