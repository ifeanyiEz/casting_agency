# Casting Agency API
This is the final project for the Full Stack Web Developer Nanodegree Program by Udacity.

## Heroku Address
The project is hosted at https://ezu-casting-agency.herokuapp.com

## Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The developer plays the role of an Executive Producer within the company and is therefore tasked with creating a system to simplify and streamline the agency's operational processes.

## Motivation for the Project
This capstone project is designed to provide an opportunity for students, who have successfully gone through the program, to use all of the concepts and skills taught in the courses to build an API from start to finish and host it.

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
In the app.py file uncomment the line that contains the function drop_and_create_all()on first run only. This will initialize the database.
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
## Endpoints:
The following are the application endpoints and the expected return outputs
#### GET '/api/v1.0/actors'
This endpoints returns a jsonified list of all the actors in the database, presented in pages of 5 actors per page. Actors' details are shown as dictionaries in the actor_long() format.
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
##### POST '/api/v1.0/actors'
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
##### PATCH '/api/v1.0/actors/${id}'

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

##### DELETE '/api/v1.0/actors/${id}'

```
{
    "deleted actor": "Actor with id: 12",
    "success": true
}
```


##### GET '/api/v1.0/movies'

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

##### GET '/api/v1.0/movies/${id}'

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

##### POST '/api/v1.0/movies'

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

##### PATCH '/api/v1.0/movies/${id}'

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
##### DELETE '/api/v1.0/movies/${id}'

```
{
    "deleted movie": "Movie with id: 9",
    "success": true
}
```


##### GET '/api/v1.0/casts'

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
##### POST '/api/v1.0/casts'

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
#### Test_App Local Run 
```
dropdb casting_test && createdb casting_test
psql casting_test < casting_test.psql
python3 test_app.py
```