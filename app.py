import os
from turtle import title
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import *

#=======================INITIALIZE THE APP===================#

#def create_app(test_config=None):
  # create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)


#=============INITIALIZE THE DATABASE===================#

'''
Uncomment the line below to initialize the database with with data from models.py. 
Do this once on first run.
'''
#drop_and_create_all()


#========================DEFINE ENDPOINTS==========================#

  #==================FOR ACTORS====================#

  #__________________List all Actors_______________#

@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def list_all_actors(payload):

  page = request.args.get('page', 1, type=int)

  try:
    all_actors = Actor.query.paginate(page = page, per_page = 10)
    if len(all_actors.items()) == 0:
      abort(404)
    actors = [actor.format_actor() for actor in all_actors]
    return jsonify({
      'success': True,
      'actors': actors
    }), 200

  except:
    abort(422)


  #__________________Get Specific Actor_______________#

@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor_by_id(payload, actor_id):
  try:
    specific_actor = Actor.query.filter_by(id = actor_id).one_or_none()
    if specific_actor is None:
      return jsonify({
        'success': False,
        'message': 'Actor with id: {} was not found'.format(actor_id)
      }), 404
    actor = specific_actor.format_actor()
    return jsonify({
      'success': True,
      'actor': actor
    }), 200
  except:
    abort(422)


  #__________________Create New Actors_______________#

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):

  data = request.get_json()
  name = data.get('name', None)
  age = data.get('age', None)
  gender = data.get('gender', None)

  try:
    if name is None or age is None or gender is None:
      return jsonify({
        'success': False,
        'message': 'The server could not understand the request. The details provided for new actor are incomplete'
      }), 400

    new_actor = Actor(name = name, age = age, gender = gender)
    new_actor.insert_actor()

    actor = new_actor.format_actor()
    return jsonify({
      'success': True,
      'new_actor': actor
    }), 200

  except:
    abort(422)


  #__________________Edit Specific Actor_______________#

@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def modify_actor(payload, actor_id):

  data = request.get_json()
  name = data.get('name', None)
  age = data.get('age', None)
  gender = data.get('gender', None)

  try:
    actor = Actor.query.filter_by(id = actor_id).one_or_None()
    if actor is None:
      return jsonify({
          'success': False,
          'message': 'Actor with id: {} was not found'.format(actor_id)
      }), 404
    if name is None and age is None and gender is None:
      return jsonify({
          'success': False,
          'message': 'The server could not understand the request. There are no details provided for actor.'
      }), 400
    elif name is not None and age is None and gender is None:
      actor.name = name
      actor.update_actor()
    elif name is None and age is not None and gender is None:
      actor.age = age
      actor.update_actor()
    elif name is None and age is None and gender is not None:
      actor.gender = gender
      actor.update_actor()
    elif name is not None and age is not None and gender is None:
      actor.name = name
      actor.age = age
      actor.update_actor()
    elif name is not None and age is None and gender is not None:
      actor.name = name
      actor.gender = gender
      actor.update_actor()
    elif name is None and age is not None and gender is not None:
      actor.age = age
      actor.gender = gender
      actor.update_actor()
    else:
      actor.name = name
      actor.age = age
      actor.gender = gender
      actor.update_actor()
    
    modified_actor = Actor.query.filter_by(id=actor_id).one_or_None()

    return jsonify({
      'success': True,
      'actor': modified_actor.format_actor()
    }), 200
    
  except:
    abort(422)


  #_________________Delete Specific Actor_______________#

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
  try:
    actor = Actor.query.filter_by(id = actor_id).one_or_none()
    if actor is None:
      return jsonify({
          'success': False,
          'message': 'Actor with id: {} was not found'.format(actor_id)
      }), 404
    actor.delete_actor()
    deleted_actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if deleted_actor is not None:
        return jsonify({
            'success': False,
            'message': 'Actor with id: {} was not deleted'.format(actor_id)
        }), 422
    else:
      deleted_actor_id = actor.id
      return jsonify({
        'success': True,
        'deleted_actor': 'Actor with id: {}'.format(deleted_actor_id)
      })
  except:
    abort(422)
  


  #==================FOR MOVIES====================#


  #__________________List all Movies_______________#

@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def list_all_movies():

  page = request.args.get('page', 1, type=int)

  try:
    all_movies = Movie.query.order_by(Movie.release_date.desc()).paginate(page = page, per_page = 10)
    if len(all_movies.items()) == 0:
      abort(404)
    formatted_movies = [movie.format_movie() for movie in all_movies]
    return jsonify({
      'success': True,
      'movies': formatted_movies
    }), 200
  except:
    abort(422)


  #__________________Get Specific Movie_______________#

@app.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie_by_id(payload, movie_id):
  try:
    specific_movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if specific_movie is None:
      return jsonify({
          'success': False,
          'message': 'Movie with id: {} was not found'.format(movie_id)
      }), 404
    movie = specific_movie.format_movie()
    return jsonify({
        'success': True,
        'actor': movie
    }), 200
  except:
    abort(422)


  #__________________Create New Movies_______________#

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):

  data = request.get_json()
  title = data.get('title', None)
  release_date = data.get('release_date', None)

  try:
    if title is None or release_date is None:
      return jsonify({
          'success': False,
          'message': 'The server could not understand the request. The details provided for new movie are incomplete'
      }), 400

    new_movie = Movie(title = title, release_date = release_date)
    new_movie.insert_movie()

    movie = new_movie.format_movie()

    return jsonify({
        'success': True,
        'new_actor': movie
    }), 200

  except:
    abort(422)


#__________________Edit Specific Movie_______________#

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def modify_movie(payload, movie_id):

  data = request.get_json()
  title = data.get('title', None)
  release_date = data.get('release_date', None)

  try:
    movie = Movie.query.filter_by(id = movie_id).one_or_None()
    if movie is None:
      return jsonify({
          'success': False,
          'message': 'Movie with id: {} was not found'.format(movie_id)
      }), 404
    if title is None and release_date is None:
      return jsonify({
          'success': False,
          'message': 'The server could not understand the request. There are no details provided for movie.'
      }), 400
    elif title is not None and release_date is None:
      movie.title = title
      movie.update_movie()
    elif title is None and release_date is not None:
      movie.release_date = release_date
      movie.update_movie()
    else:
      movie.title = title
      movie.release_date = release_date
      movie.update_movie()

    modified_movie = Movie.query.filter_by(id=movie_id).one_or_None()

    return jsonify({
        'success': True,
        'movie': modified_movie.format_movie()
    }), 200

  except:
    abort(422)


#_________________Delete Specific Movie_______________#

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
  try:
    movie = Movie.query.filter_by(id = movie_id).one_or_none()
    if movie is None:
      return jsonify({
          'success': False,
          'message': 'Movie with id: {} was not found'.format(movie_id)
      }), 404
    movie.delete_movie()
    deleted_movie = Movie.query.filter_by(id = movie_id).one_or_none()
    if deleted_movie is not None:
        return jsonify({
            'success': False,
            'message': 'Movie with id: {} was not deleted'.format(movie_id)
        }), 422
    else:
      deleted_movie_id = movie.id
      return jsonify({
          'success': True,
          'deleted_movie': 'Movie with id: {}'.format(deleted_movie_id)
      })
  except:
    abort(422)



#======================ERROR HANDLING=====================#

@app.errorhandler(400)
def bad_request(error):
  return jsonify({
      "success": False,
      "error": 400,
      "message": "The server could not understand the request due to invalid syntax."
  }), 400

@app.errorhandler(401)
def unauthorized(error):
  return jsonify({
      "success": False,
      "error": 401,
      "message": "Client must authenticate itself to get the requested resource."
  }), 401
  
@app.errorhandler(403)
def forbiden(error):
  return jsonify({
      "success": False,
      "error": 403,
      "message": "Client does not have access rights to the requested resource"
  }), 403

@app.errorhandler(404)
def not_found(error):
  return jsonify({
      "success": False,
      "error": 404,
      "message": "The server can not find the requested resource"
  }), 404

@app.errorhandler(405)
def method_not_allowed(error):
  return jsonify({
      "success": False,
      "error": 405,
      "message": "This method is not allowed for the requested URL"
  }), 405

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
      "success": False,
      "error": 422,
      "message": "The request was unable to be followed due to semantic errors"
  }), 422

@app.errorhandler(500)
def internal_error(error):
  return jsonify({
      "success": False,
      "error": 500,
      "message": "The server has encountered an internal error"
  }), 500

@app.errorhandler(AuthError)
def handle_auth_error(exception):
  response = jsonify(exception.error)
  response.status_code = exception.status_code
  return response
  
  #return app

#APP = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)