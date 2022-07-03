import os
import unittest
import json
from urllib import response
from jose import jwt
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

        self.casting_assistant = CASTING_ASSISTANT_TOKEN
        self.casting_director = CASTING_DIRECTOR_TOKEN
        self.executive_producer = EXECUTIVE_PRODUCER_TOKEN

        setup_db(self.app, self.database_path)

        self.first_movie = {
            'title': 'A Heart Full Of Dreams',
            'release_date': 'June 12, 2023'
            }

        self.second_movie = {
            'title': '',
            'release_date': 'June 12, 2023'
        }

        self.third_movie = {
            'title': 'A Broken Rose',
            'release_date': 'June 12, 2023'
        }

        self.fourth_movie = {
            'title': 'A Broken Rose',
        }

        self.fifth_movie = {
            'title': 'Osuofia inside London',
            'release_date': '2023-01-25 15:20:00'
        }

        self.sixth_movie = {
            'title': 'A Heart Full Of Dreams',
            'release_date': ''
        }

        self.first_actor = {
            'name': 'Emmanuel Black',
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

        self.fifth_actor = {
            'name': 'Nicolas Cage'
        }

        self.sixth_actor = {
            'name': '',
            'age': 36,
            'gender': ''
        }

        self.first_cast = {
            'actor_id': 1,
            'movie_id': 8
        }

        self.second_cast = {
            'actor_id': 1,
            'movie_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

#================OPERATIONAL TESTS====================================#


    #======================TESTS FOR ACTORS=========================#


    #____________Create New Actor: Correct Data___________________#

    def test_create_correct_actor(self):
        '''Check if actors are created as expected with correct data'''
        response = self.client().post(
            '/actors', 
            json=self.first_actor, 
            headers = {'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new actor'])


    #____________Create New Actor: Incorrect Data___________________#

    def test_create_incorrect_actor(self):
        '''Check if actors are created even with missing details'''
        response = self.client().post(
            '/actors', 
            json=self.second_actor,
            headers = {'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    #____________Create New Actor: Non-uniqe Data___________________#

    def test_create_non_unique_actor(self):
        '''Check if actors are created only with unique names'''
        response = self.client().post(
            '/actors', 
            json = self.third_actor,
            headers={'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)


    #____________Create New Actor: Incomplete Data___________________#

    def test_create_incomplete_actor(self):
        '''Check if actors are created even with missing data'''
        response = self.client().post(
            '/actors', 
            json=self.fourth_actor,
            headers={'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    #___________________List ALl Actors___________________#

    def test_list_actors(self):
        '''Check to see if all actors are listed as expected'''
        response = self.client().get(
            '/actors',
            headers = {'Authorization': 'Bearer {}'.format(self.casting_assistant)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['all_actors'])


    #__________________Get Specific Actor: Correct ID_________________#

    def test_get_specific_actor(self):
        '''Check to see if a specific actor can be found, given the actor's ID'''
        response = self.client().get(
            '/actors/9',
            headers = {'Authorization': 'Bearer {}'.format(self.casting_assistant)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(data['featured in'])


    #__________________Get Specific Actor: Incorrect ID_________________#

    def test_get_wrong_actor(self):
        '''Check to see if non-existent actors can be found, given the actor ID'''
        response = self.client().get(
            '/actors/20',
            headers = {'Authorization': 'Bearer {}'.format(self.casting_assistant)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Actor with id: 20 was not found')


    #__________________Edit Specific Actor: Correct Data_______________#

    def test_edit_specific_actor(self):
        '''Check to see if actors are patched with new data as expected'''
        response = self.client().patch(
            '/actors/10', 
            json = self.fifth_actor,
            headers = {'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['modified actor'])


    #__________________Edit Specific Actor: Incorrect Data_______________#

    def test_edit_incorrect_data_actor(self):
        '''Check to see if actors are not patched with incorrect data as expected'''
        response = self.client().patch(
            '/actors/11', 
            json=self.sixth_actor,
            headers = {'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    #_________________Delete Specific Actor: Valid Actor ID_________________#

    def test_delete_specific_actor(self):
        '''Check to see if actors are deleted as expected, given valid actor ID'''
        response = self.client().delete(
            '/actors/8',
            headers = {'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted actor'])
        self.assertEqual(data['deleted actor'], 'Actor with id: 8')


    #_________________Delete Specific Actor: Invalid Actor ID_________________#

    def test_delete_invalid_actor(self):
        '''Check to see if the system responds as expected, given an invalid actor ID'''
        response = self.client().delete(
            '/actors/20',
            headers = {'Authorization': 'Bearer {}'.format(self.casting_director)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Actor with id: 20 was not found')


        

    #========================TESTS FOR MOVIES=============================#


    #____________Create New Movie: Correct Data___________________#

    def test_create_correct_movie(self):
        '''Check if movies are created as expected with correct data'''
        response = self.client().post(
            '/movies', 
            json=self.first_movie,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new movie'])


    #____________Create New Movie: Incorrect Data___________________#

    def test_create_incorrect_movie(self):
        '''Check if movies are created even with missing details'''
        response = self.client().post(
            '/movies', 
            json=self.second_movie,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    #____________Create New Movie: Non-uniqe Data___________________#

    def test_create_non_unique_movie(self):
        '''Check if movies are created only with unique titles'''
        response = self.client().post(
            '/movies', 
            json=self.third_movie,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)


    #____________Create New Movie: Incomplete Data___________________#

    def test_create_incomplete_movie(self):
        '''Check if movies are created even with missing data'''
        response = self.client().post(
            '/movies', 
            json=self.fourth_movie,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    #___________________List ALl Movies___________________#

    def test_list_movies(self):
        '''Check to see if all movies are listed as expected'''
        response = self.client().get(
            '/movies',
            headers = {'Authorization': 'Bearer {}'.format(self.casting_assistant)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['all_movies'])


    #__________________Get Specific Movie: Correct ID_________________#

    def test_get_specific_movie(self):
        '''Check to see if a specific movie can be found, given the movie ID'''
        response = self.client().get(
            '/movies/9',
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(data['featured actors'])


    #__________________Get Specific Movie: Incorrect ID_________________#

    def test_get_wrong_movie(self):
        '''Check to see if a non-existent movie can be found, given the movie ID'''
        response = self.client().get(
            '/movies/20',
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Movie with id: 20 was not found')


    #__________________Edit Specific Movie: Correct Data_______________#

    def test_edit_specific_movie(self):
        '''Check to see if movies are patched with new data as expected'''
        response = self.client().patch(
            '/movies/10', 
            json = self.fifth_movie,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['modified movie'])


    #__________________Edit Specific Movie: Incorrect Data_______________#

    def test_edit_incorrect_data_movie(self):
        '''Check to see if movies are not patched with incorrect data as expected'''
        response = self.client().patch(
            '/movies/11', 
            json = self.sixth_movie,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    #_________________Delete Specific Movie: Valid Movie ID_________________#

    def test_delete_specific_movie(self):
        '''Check to see if movies are deleted as expected, given valid movie ID'''
        response = self.client().delete(
            '/movies/8',
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted movie'])
        self.assertEqual(data['deleted movie'], 'Movie with id: 8')

    #_________________Delete Specific Movie: Invalid Movie ID_________________#

    def test_delete_invalid_movie(self):
        '''Check to see if the system responds as expected, given an invalid movie ID'''
        response = self.client().delete(
            '/movies/20',
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Movie with id: 20 was not found')




    #=================TESTS FOR CASTS ENDPOINTS========================#

    #____________Create New Cast: Correct Data___________________#

    def test_create_correct_cast(self):
        '''Check if casts are created as expected with correct data'''
        response = self.client().post(
            '/casts', 
            json=self.first_cast,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new movie cast'])


    #____________Create New Cast: Already Existing Cast___________________#

    def test_create_existing_cast(self):
        '''Check if casts are created uniquely as expected'''
        response = self.client().post(
            '/casts',
             json=self.second_cast,
            headers = {'Authorization': 'Bearer {}'.format(self.executive_producer)}
             )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'This actor has already been cast for this movie.')
        

    #___________________List ALl Casts___________________#

    def test_list_casts(self):
        '''Check to see if all casts are listed as expected'''
        response = self.client().get(
            '/casts',
            headers = {'Authorization': 'Bearer {}'.format(self.casting_assistant)}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cast_details'])
        self.assertTrue(data['total casts'])


#================MAKE THE TESTS EXECUTABLE====================#

if __name__ == "__main__":
    unittest.main()
