
import os
from flask import session
from sqlalchemy import Column, String, Integer, create_engine, delete
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
from settings import *
import json


#database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, 'localhost:5432', DB_NAME)

database_path = DB_URL
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    This will bind a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
drop_and_create_all()
This is designed for initializing the database. 
It will drop all data from the DB and create fresh entries. 
'''
def drop_and_create_all():
    db.drop_all()
    db.create_all()

    first_movie = Movie(
        title='A Broken Rose', 
        release_date='June 12, 2023'
        )
    first_movie.insert_movie()

    second_movie = Movie(
        title='On These Matters', 
        release_date='July 22, 2023'
        )
    second_movie.insert_movie()

    third_movie = Movie(
        title='Third Wrong', 
        release_date='August 12, 2022'
        )
    third_movie.insert_movie()

    first_actor = Actor(
        name='Amarachi Ezgels', 
        age=36, 
        gender='Female'
        )
    first_actor.insert_actor()

    second_actor = Actor(
        name='Bukky Jasa', 
        age=30, 
        gender='Female'
        )
    second_actor.insert_actor()

    third_actor = Actor(
        name='Anyi Gwoke', 
        age=12, 
        gender='Male'
        )
    third_actor.insert_actor()

    first_cast = Movie_Cast.insert().values(
        actor_id=1, 
        movie_id=2
        )
    db.session.execute(first_cast)
    db.session.commit()



'''An association table connects the Movie model with the Actor model.
A movie session provides the avenue for one or more actors to take part in a move.
One movie may involve several actors, while one actor may appear in several movies.
'''

Movie_Cast = db.Table('movie_casts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), nullable=False),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), nullable=False)
    )


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    actor = db.relationship('Actor', secondary=Movie_Cast, lazy='select', backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert_movie(self):
        db.session.add(self)
        db.session.commit()

    def update_movie(self):
        db.session.commit()

    def delete_movie(self):
        db.session.delete(self)
        db.session.commit()

    def movie_detail(self):
        return{
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

    def movie_short(self):
        return{
            "movie": 'Title: {}, Release Date: {}'.format(self.title, self.release_date)
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert_actor(self):
        db.session.add(self)
        db.session.commit()

    def update_actor(self):
        db.session.commit()

    def delete_actor(self):
        db.session.delete(self)
        db.session.commit()

    def actor_detail(self):
        return{
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }
    
    def actor_short(self):
        return{
            "actor": 'Name: {}, Age: {}, Gender: {}'.format(self.name, self.age, self.gender)
        }
