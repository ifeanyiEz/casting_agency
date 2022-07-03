
import os
import sys
from turtle import title
from jose import jwt
from flask import Flask, Request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import *
import settings

#=======================INITIALIZE THE APP===================#

def create_app(test_config=None):
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
      all_actors = Actor.query.order_by(Actor.id).paginate(page = page, per_page = 5)
      if len(all_actors.items) == 0:
        abort(404)
      actors = [actor.actor_detail() for actor in all_actors.items]
      return jsonify({
        'success': True,
        'actors': actors,
        'all_actors': all_actors.total
      }), 200

    except:
      print(sys.exc_info())
      abort(422)


    #__________________Get Specific Actor_______________#

  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('get:actors')
  def get_specific_actor(payload, actor_id):
    try:
      specific_actor = Actor.query.filter_by(id = actor_id).one_or_none()
      if specific_actor is None:
        return jsonify({
          'success': False,
          'message': 'Actor with id: {} was not found'.format(actor_id)
        }), 404
      actor = specific_actor.actor_detail()

      movies_featured_in = []

      all_movie_casts = db.session.query(Movie_Cast).filter_by(actor_id = actor_id).all()
      if len(all_movie_casts) == 0:
        return jsonify({
            'success': True,
            'actor': actor,
            'featured in': 'This actor has not featured in any movie yet'
        }), 200

      for movie_cast in all_movie_casts:
        featured_movie = Movie.query.filter_by(id = movie_cast.movie_id).one_or_none()
        movies_featured_in.append(featured_movie.movie_short())

      return jsonify({
        'success': True,
        'actor': actor,
        'featured in': movies_featured_in
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

      elif len(name) == 0 or len(str(age)) == 0 or len(gender) == 0:
        return jsonify({
          'success': False,
          'message': 'The server could not understand the request. You must provide valid data to add an actor'
        }), 400

      else:
        new_actor = Actor(name = name, age = age, gender = gender)
        new_actor.insert_actor()

      actor = new_actor.actor_detail()

      return jsonify({
        'success': True,
        'new actor': actor
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
      actor = Actor.query.filter_by(id = actor_id).first_or_404()
      if actor is None:
        return jsonify({
            'success': False,
            'message': 'Actor with id: {} was not found'.format(actor_id)
        }), 404

      empty_string_error = jsonify({
          'success': False,
          'message': 'The server could not understand the request. Details for actors cannot be empty.'
        }), 400

      if name is None and age is None and gender is None:
        return jsonify({
            'success': False,
            'message': 'The server could not understand the request. You must provide valid data for actor.'
        }), 400

      elif name is not None and age is None and gender is None:
        if len(name) != 0:
          actor.name = name
          actor.update_actor()
        else:
          return empty_string_error

      elif name is None and age is not None and gender is None:
        if len(str(age)) != 0:
          actor.age = age
          actor.update_actor()
        else:
          return empty_string_error

      elif name is None and age is None and gender is not None:
        if len(gender) != 0:
          actor.gender = gender
          actor.update_actor()
        else:
          return empty_string_error
      
      elif name is not None and age is not None and gender is None:
        if len(name) != 0 and len(str(age)) != 0:
          actor.name = name
          actor.age = age
          actor.update_actor()
        else:
          return empty_string_error

      elif name is not None and age is None and gender is not None:
        if len(name) != 0 and len(gender) != 0:
          actor.name = name
          actor.gender = gender
          actor.update_actor()
        else:
          return empty_string_error

      elif name is None and age is not None and gender is not None:
        if len(str(age)) != 0 and len(gender) != 0:
          actor.age = age
          actor.gender = gender
          actor.update_actor()
        else:
          return empty_string_error

      else:
        if len(name) != 0 and len(str(age)) != 0 and len(gender) != 0:
          actor.name = name
          actor.age = age
          actor.gender = gender
          actor.update_actor()
        else:
          return empty_string_error
      
      modified_actor = Actor.query.filter_by(id = actor_id).first_or_404()

      return jsonify({
        'success': True,
        'modified actor': modified_actor.actor_detail()
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
              'message': 'Actor with id: {} was not deleted. Please try again.'.format(actor_id)
          }), 422
      else:
        deleted_actor_id = actor.id
        return jsonify({
          'success': True,
          'deleted actor': 'Actor with id: {}'.format(deleted_actor_id)
        })
    except:
      abort(422)
    


    #==================FOR MOVIES====================#


    #__________________List all Movies_______________#

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def list_all_movies(payload):

    page = request.args.get('page', 1, type=int)

    try:
      all_movies = Movie.query.order_by(Movie.release_date.asc()).paginate(page = page, per_page = 5)
      if len(all_movies.items) == 0:
        abort(404)
      formatted_movies = [movie.movie_detail() for movie in all_movies.items]
      return jsonify({
        'success': True,
        'movies': formatted_movies,
        'all_movies': all_movies.total
      }), 200
    except:
      abort(422)


    #__________________Get Specific Movie_______________#

  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth('get:movies')
  def get_specific_movie(payload, movie_id):
    try:
      specific_movie = Movie.query.filter_by(id = movie_id).one_or_none()
      if specific_movie is None:
        return jsonify({
            'success': False,
            'message': 'Movie with id: {} was not found'.format(movie_id)
        }), 404
      movie = specific_movie.movie_detail()

      all_featured_actors = []

      all_movie_cast = db.session.query(Movie_Cast).filter_by(movie_id = movie_id).all()
      if len(all_movie_cast) == 0:
        return jsonify({
          'success': True,
          'movie': movie,
          'featured actors': 'No actors have been cast for this movie'
        }), 200
      
      for movie_cast in all_movie_cast:
        featured_actor = Actor.query.filter_by(id = movie_cast.actor_id).one_or_none()
        all_featured_actors.append(featured_actor.actor_short())
      
      return jsonify({
          'success': True,
          'movie': movie,
          'featured actors': all_featured_actors
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

      elif len(title) == 0 or len(str(release_date)) == 0:
        return jsonify({
            'success': False,
            'message': 'The server could not understand the request. You must provide valid data to add a movie'
          }), 400

      else:
        new_movie = Movie(title = title, release_date = release_date)
        new_movie.insert_movie()

      movie = new_movie.movie_detail()

      return jsonify({
          'success': True,
          'new movie': movie
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
      movie = Movie.query.filter_by(id = movie_id).first_or_404()
      if movie is None:
        return jsonify({
            'success': False,
            'message': 'Movie with id: {} was not found'.format(movie_id)
        }), 404

      empty_string_error = jsonify({
          'success': False,
          'message': 'The server could not understand the request. Details for movies cannot be empty.'
        }), 400

      if title is None and release_date is None:
        return jsonify({
            'success': False,
            'message': 'The server could not understand the request. There are no details provided for movie.'
        }), 400

      elif title is not None and release_date is None:
        if len(title) != 0:
          movie.title = title
          movie.update_movie()
        else:
          return empty_string_error

      elif title is None and release_date is not None:
        if len(release_date) != 0:
          movie.release_date = release_date
          movie.update_movie()
        else:
          return empty_string_error

      else:
        if len(title) != 0 and len(release_date) != 0:
          movie.title = title
          movie.release_date = release_date
          movie.update_movie()
        else:
          return empty_string_error

      modified_movie = Movie.query.filter_by(id = movie_id).first_or_404()

      return jsonify({
          'success': True,
          'modified movie': modified_movie.movie_detail()
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
              'message': 'Movie with id: {} was not deleted. Please try again.'.format(movie_id)
          }), 422
      else:
        deleted_movie_id = movie.id
        return jsonify({
            'success': True,
            'deleted movie': 'Movie with id: {}'.format(deleted_movie_id)
        })

    except:
      abort(422)


    #==================FOR CASTING SESSIONS====================#

    #__________________List all Movie Casts_______________#

  @app.route('/casts', methods=['GET'])
  @requires_auth('get:movie_casts')
  def list_movie_casts(payload):

    try:

      page = request.args.get('page', 1, type=int)
      cast_info = []

      all_casts = db.session.query(Movie_Cast).paginate(page = page, per_page = 5)
      if len(all_casts.items) == 0:
        return jsonify({
          'success': False,
          'message': 'No casting records were found'
        }), 404

      else:
        for each_cast in all_casts.items:
          movie = Movie.query.filter_by(id = each_cast.movie_id).first()
          actor = Actor.query.filter_by(id = each_cast.actor_id).first()

          cast_info.append({
            'movie_id': each_cast.movie_id,
            'movie_title': movie.title,
            'movie_release_date': movie.release_date.strftime("%B %d %Y %H:%M:%S"),
            'actor_id': each_cast.actor_id,
            'actor_name': actor.name,
            'actor_age': actor.age,
            'actor_gender': actor.gender
          })

      return jsonify({
        'success': True,
        'cast_details': cast_info,
        'total casts': all_casts.total
      }), 200

    except:
      abort(422)



    #__________________Create Movie Casts_______________#

  @app.route('/casts', methods=['POST'])
  @requires_auth('post:movie_casts')
  def create_cast(payload):

    data = request.get_json()
    actor_id = data.get('actor_id', None)
    movie_id = data.get('movie_id', None)
    
    try:
      
      if actor_id is None or movie_id is None:
        return jsonify({
          'success': False,
          'message': 'The server could not understand the request. There are no details provided for this cast.'
        }), 400
      
      check_actor = Actor.query.filter_by(id = actor_id).first()
      check_movie = Movie.query.filter_by(id = movie_id).first()

      if check_actor is None or check_movie is None:
        return jsonify({
          'success': False,
          'message': 'One or both details does not exist in the database. Please reconfirm then proceed'
        }), 400
      
      check_cast = db.session.query(Movie_Cast).filter_by(actor_id = actor_id, movie_id = movie_id).first()
      if check_cast is not None:
        return jsonify({
            'success': False,
            'message': 'This actor has already been cast for this movie.'
        }), 400

      else:
        movie_cast = Movie_Cast.insert().values(actor_id = actor_id, movie_id = movie_id)
        db.session.execute(movie_cast)
        db.session.commit()

      new_cast = db.session.query(Movie_Cast).filter_by(actor_id = actor_id, movie_id = movie_id).first()
      if new_cast is None:
        return jsonify({
            'success': False,
            'message': 'The movie cast was not created, please try again.'
        }), 400
      else:
        new_movie_cast = {}
        new_movie_cast['id'] = new_cast.id
        new_movie_cast['actor_id'] = new_cast.actor_id
        new_movie_cast['movie_id'] = new_cast.movie_id

      return jsonify({
        'success': True,
        'new movie cast': new_movie_cast
      }), 200

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
  
  return app

app = create_app()

if __name__ == '__main__':
    app.run()