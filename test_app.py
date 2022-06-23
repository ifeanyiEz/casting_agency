import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy
from settings import *
from models import *
from app import create_app


#==============DEFINE THE CASTING AGENCY TEST CASE=================#

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        '''Define test variable and initialize the test app'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.first_movie = {
            'title': 'A Broken Rose',
            'release_date': 'June 12, 2023'
            }

        self.first_actor = {
            'name': 'Harrison Ezgels',
            'age': 36,
            'gender': 'Male'
            }

        self.second_actor = {
            'name': '',
            'age': 36,
            'gender': 'Male'
        }

        self.third_actor = {
            'name': 'Harrison Ezgels',
            'age': 36,
            'gender': 'Male'
        }

        self.fourth_actor = {
            'age': 36,
            'gender': 'Male'
        }

        self.first_cast = {
            'actor_id': 1,
            'movie_id': 2
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

#================OPERATIONAL TESTS============================#

    #____________Create New Actor: Correct Data___________________#

    def test_create_correct_actor(self):
        '''Check if actors are created as expected with correct data'''
        response = self.client().post('/actors', json=self.first_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actor'])


    #____________Create New Actor: Incorrect Data___________________#

    def test_create_incorrect_actor(self):
        '''Check if actors are created even with missing details'''
        response = self.client().post('/actors', json=self.second_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


    #____________Create New Actor: Nonuniqe Data___________________#

    def test_create_nonunique_actor(self):
        '''Check if actors are created only with unique names'''
        response = self.client().post('/actors', json = self.third_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)


#____________Create New Actor: Incomplete Data___________________#

    def test_create_incomplete_actor(self):
        '''Check if actors are created even with missing data'''
        response = self.client().post('/actors', json=self.fourth_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

#================MAKE THE TESTS EXECUTABLE====================#

if __name__ == "__main__":
    unittest.main()
