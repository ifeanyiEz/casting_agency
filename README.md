# Casting Agency API
This is the final project for the Full Stack Web Developer Nanodegree Program by Udacity.

## Heroku Address
The project is hosted at https://ezu-casting-agency.herokuapp.com

## Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The developer plays the role of an Executive Producer within the company and is therefore tasked with creating a system to simplify and streamline the agency's operational processes.

## Motivation for the Project
This capstone project is designed to provide an opportunity for students, who have successfully gone through the program, to use all of the concepts and skills taught in the courses to build an API from start to finish and host it.
## Project file structure
The project is structured as follows:
```
├── capstone/
├── .env
├── .gitignore
├── app.py
├── auth.py
├── casting_test.psql
├── Manage,py
├── models.py
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
└── settings.py
├── setup.sh
└── test_app.py
```
## Database Classes
The database comprises the Actor and Movie classes which inherit from db.Model, as well as a Movie_Cast table (db.Table) wchich is the association between actors and movies.

## User Roles
There are three (3) user roles for this project:

#### Casting Assistant
Offers general help with finding actors to star in a movie. This role can view actors, movies and casts.
```
get:actors
get:movies
get:movie_casts
```
#### Casting Director
Casting directors find the stars who bring the characters in a movie to life. This role has all the permissions of the casting assistant, plus the permission to create, modifiy and delete actors, as well as modify movies. 
```
get:actors
post:actors
patch:actors
delete:actors
get:movies
patch:movies
get:movie_casts
```
#### Executive Producer
Executive producers finance the movies, participate in the creative effort, or work on set. Their responsibilities vary from funding or attracting investors into the movie project to legal, scripting, marketing, advisory and supervising capacities. This role has all the permissions of a casting director plus the permission to create movie casts, as well as to create and delete movies.
```
get:actors
post:actors
patch:actors
delete:actors
get:movies
patch:movies
post:movies
delete:movies
get:movie_casts
post:movie_casts
```
## Running the Project Locally
In order to successfully run the project on your local server, you'd need to pay attention to the following:

#### Install Python3.9
This project was created using python3.9. In order to install the latest version of python, follow the instructions at https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python
#### Create a Virtual Environment
For best results and performance, it is strongly recommended all python projects should be run in virtual environments. This allows you to stay organized and isolate each project with it's uniques set of dependencies.

To create your uniquely named virtual environment run
```
python3 -m venv <env_name>
```
To activate the environment so as to begin working from within the environment, run
```
source <env_name>/bin/activate
```
#### Install Dependencies
To install dependencies run
```
pip install -r requirements.txt
```
#### Setup The Database
With Postgres running, create the database using the following command: 
```
createdb casting_agency
```
#### Initialize the Database
In the app.py file uncomment the line that contains the function drop_and_create_all() on first run only. This will initialize the database. Comment this line out after the first run.
#### App Local Run
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```
## Actors and Movies Formats
Actors and Movies are presented in the detailed or short formats, depending on the endpoint and the need for information.
#### Detailed Actor Format
The actor_detail() output format looks like this:
```
{
    "id": 20,
    "name": "Amarachi Ezgels"
    "age": 37,
    "gender": "Female"
}
```
#### Short Actor Format
The actor_short() output format looks like this:
```
{
    "actor": "Name: Amarachi Ezgels, Age: 37, Gender: Female"
}
```
#### Detailed Movie Format
The movie_detail() output format looks like this:
```
{
    "id": 24,
    "title": "This Movie Title",
    "release_date": "2023-07-22 00:00:00"
}
```
#### Short Movie Format
The movie_short() output format looks like this:
```
{
    "movie": "Title: This Movie Title, Release Date: 2023-07-22 00:00:00"
}
```
## API Endpoints Behaviour:
The following are the application endpoints and the expected return outputs
### Actors
#### GET '/api/v1.0/actors'
This endpoints returns a jsonified list of all the actors in the database, presented in pages of 5 actors per page. Actors' details are shown as dictionaries in the actor_detail() format.
It also includes the total number of actors in the database, as shown in the sample:
```
{
    "actors": [
        {
            "age": 36,
            "gender": "Female",
            "id": 1,
            "name": "Amarachi Ezgels"
        },
        {
            "age": 30,
            "gender": "Female",
            "id": 2,
            "name": "Bukky Jasa"
        },
        {
            "age": 32,
            "gender": "Male",
            "id": 3,
            "name": "Chibzi Gwoke"
        }
    ],
    "all_actors": 10
    "success": true
}
```
#### GET '/api/v1.0/actors/${id}'
This end point returns a jsonified output for a specific actor in the database. The output presents the actor's details in a dict and includes all the movies featuring the requested actor in an array, in which each movie is presented in the movie_short() format.
```
{
    "actor": {
        "age": 32,
        "gender": "Male",
        "id": 3,
        "name": "Chibzi Gwoke"
    },
    "featured in": [
        {
            "movie": "Title: Third Wrong, Release Date: 2022-08-12 00:00:00"
        },
        {
            "movie": "Title: On These Matters, Release Date: 2023-07-22 00:00:00"
        },
        {
            "movie": "Title: A Broken Rose, Release Date: 2023-06-12 00:00:00"
        }
    ],
    "success": true
}
```
#### POST '/api/v1.0/actors'
This endpoint creates and sends the data of a new actor into the DB and, for a successful addition, it returns a jsonified output showing the details of the actor. Actors are uniquely created by name.
```
{
    "new actor": {
        "age": 45,
        "gender": "Male",
        "id": 11,
        "name": "Anyi Ezgels"
    },
    "success": true
}
```
#### PATCH '/api/v1.0/actors/${id}'
This endpoint modifies the details of a specific existing actor and, for a successful patch, returns the details of the modified actor in the actor_detail() format.
```
{
    "modified actor": {
        "age": 39,
        "gender": "Female",
        "id": 12,
        "name": "Edith Onwer"
    },
    "success": true
}
```
#### DELETE '/api/v1.0/actors/${id}'
This endpoint removes the record of a specific existing actor from the database. If the deletion is successful, it returns the ID of the deleted actor.
```
{
    "deleted actor": "Actor with id: 12",
    "success": true
}
```
### Movies
#### GET '/api/v1.0/movies'
This endpoints returns a jsonified list of all the movies in the database, presented in pages of 5 movies per page. Movies' details are shown as dictionaries in the movie_detail() format.
It also includes the total number of movies in the database, as shown in the sample:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 12 Jun 2023 00:00:00 GMT",
            "title": "A Broken Rose"
        },
        {
            "id": 2,
            "release_date": "Sat, 22 Jul 2023 00:00:00 GMT",
            "title": "On These Matters"
        },
        {
            "id": 3,
            "release_date": "Fri, 12 Aug 2022 00:00:00 GMT",
            "title": "Third Wrong"
        }
    ],
    "all_movies": 17
    "success": true
}
```
#### GET '/api/v1.0/movies/${id}'
This end point returns a jsonified output for a specific movie in the database. The output presents the movie's details in a dict and includes all the actors featured the requested movie in an array, in which each actor is presented in the actor_short() format.
```
{
    "movie": {
        "id": 1,
        "release_date": "Mon, 12 Jun 2023 00:00:00 GMT",
        "title": "A Broken Rose"
    },
    "featured actors": [
        {
            "actor": "Name: Amarachi Ezgels, Age: 36, Gender: Female"
        },
        {
            "actor": "Name: Bukky Jasa, Age: 30, Gender: Female"
        },
        {
            "actor": "Name: Pentium Gerald, Age: 36, Gender: Male"
        },
        {
            "actor": "Name: Chibzi Gwoke, Age: 32, Gender: Male"
        }
    ],
    "success": true
}
```
#### POST '/api/v1.0/movies'
This endpoint creates and sends the data of a new movie into the DB and, for a successful addition, it returns a jsonified output showing the details of the movie. Movies are uniquely created by name.
```
{
    "new movie": {
        "id": 6,
        "release_date": "Fri, 22 Jul 2022 00:00:00 GMT",
        "title": "The Future Of ..."
    },
    "success": true
}
```
#### PATCH '/api/v1.0/movies/${id}'
This endpoint modifies the details of a specific existing movie and, for a successful patch, returns the details of the modified movie in the movie_detail() format.
```
{
    "modified movie": {
        "id": 8,
        "release_date": "Tue, 06 Jun 2023 00:00:00 GMT",
        "title": "Avatar 2"
    },
    "success": true
}
```
#### DELETE '/api/v1.0/movies/${id}'
This endpoint removes the record of a specific existing movie from the database. If the deletion is successful, it returns the ID of the deleted movie.
```
{
    "deleted movie": "Movie with id: 9",
    "success": true
}
```
### Casts
#### GET '/api/v1.0/casts'
This endpoints returns a jsonified list of all movie casts in the database, presented in pages of 5 movie casts per page. Cast details are shown as dictionaries. It also includes the total number of casts in the database, as shown in the sample:
```
{
    "cast_details": [
        {
            "actor_age": 36,
            "actor_gender": "Female",
            "actor_id": 1,
            "actor_name": "Amarachi Ezgels",
            "movie_id": 2,
            "movie_release_date": "July 22 2023 00:00:00",
            "movie_title": "On These Matters"
        },
        {
            "actor_age": 36,
            "actor_gender": "Female",
            "actor_id": 1,
            "actor_name": "Amarachi Ezgels",
            "movie_id": 1,
            "movie_release_date": "June 12 2023 00:00:00",
            "movie_title": "A Broken Rose"
        },
        {
            "actor_age": 36,
            "actor_gender": "Female",
            "actor_id": 1,
            "actor_name": "Amarachi Ezgels",
            "movie_id": 3,
            "movie_release_date": "August 12 2022 00:00:00",
            "movie_title": "Third Wrong"
        },
    ],
    "total casts": 28
    "success": true
}
```
#### POST '/api/v1.0/casts'
This endpoint creates and sends the data of a new movie casts into the DB and, for a successful addition, it returns a jsonified output showing the details of the new movie cast.
```
{
    "new movie cast": {
        "actor_id": 11,
        "id": 26,
        "movie_id": 6
    },
    "success": true
}
```
## Test_App Local Run 
In order to run the unit tests, the following instructions are run in the terminal. These will reset the databse and ensure that it is empty, then populate it with data from the back-up copy of the casting_test db, and then run the test_app.py file: 
```
dropdb casting_test && createdb casting_test
psql casting_test < casting_test.psql
python3 test_app.py
```
## Pushing to GitHub Repository
If everything runs smoothly and all endpoints return the required outputs, the user can then push to the github repository
```
git push -u origin master
```
## Pushing to Heroku
This documentation assumes that the user already:
* Has a heroku account. The free account option would suffice for this project
* Has downloaded and installed the heroku command line interface locally, and
* Is able to login to heroku from the command line
### Login to Heroku
Use the heroku login command to login to heroku via the command line:
```heroku login -i
```
### Procfile and runtime.txt files
Before pushing the project to heroku, ensure that a runtime.txt file and a Procfile are present in the project's root directory.
#### Procfile
The procfile contains instructions to run the application using the production-ready WSGI server gunicorn, as follows:
```
web: gunicorn app:app
```
#### Runtime.txt
THis file simply states the exact python version used for the project. In this case:
```
python-3.9.7
```
### Create the project in heroku cloud
Next, while still logged in to heroku, create an app in heroku cloud. Ensure that your app has a unique name. In this case ezu-casting-agency.
```
heroku create ezu-casting-agency --buildpack heroku/python
```
### Git repository on Heroku
Ensure that a Git remote repository was created on Heroku byt the "heroku create" command.
```
git remote -v
```
### Create a postgreSQL addon for the database
Heroku has an addon for apps for a postgresql database instance. Run the following line of code in order to create the database and connect it to the application:
```
heroku addons:create heroku-postgresql:hobby-dev --app ezu-casting-agency
```
### Configure the application
In order to set up the environment variables in the Heroku cloud, specific to the application, run the following command to fix the DATABASE_URL configuration variable:
```
heroku config --app ezu-casting-agency
```
### Update .env, models.py and setup.sh files
Copy the resulting DATABASE_URL from the above step and set it as a string literal to the DATABASE_URL variable in the .env adn setup.sh files in the project root. Ensure that the databse path in models.py points to the DATABASE_URL variable.
Remember to set the EXCITED variable to 'true' from the heroku dashboard.

### Push to Heroku
Fianlly, commit the changes made to the above files, and then push the project to Heroku.
```
git push heroku master
```
## Confirm a successful build
To confirm that the push was successful navigate to the 'More' button on your application page. Select the 'Run Console' button. Then type 'bash'. After it loads up, run the following commands:
```
export FLASK_APP=app.py
export FLASK_ENV=development
python3 app.py
```
If the app starts at http://127.0.0.1:5000 without errors, then your build was successful and you can click on 'Open app' from your dashboard to open the app in the designated url.