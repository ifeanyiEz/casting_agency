App Local run

export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload

Test_app local run 

dropdb casting_test && createdb casting_test
python3 test_app.py


Endpoints:
GET '/api/v1.0/actors'

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

        '''
    ],
    "success": true
}


GET '/api/v1.0/actors/${id}'

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

POST '/api/v1.0/actors'

{
    "new_actor": {
        "age": 45,
        "gender": "Male",
        "id": 11,
        "name": "Anyi Ezgels"
    },
    "success": true
}


PATCH '/api/v1.0/actors/${id}'

{
    "modified_actor": {
        "age": 39,
        "gender": "Female",
        "id": 12,
        "name": "Edith Onwer"
    },
    "success": true
}

DELETE '/api/v1.0/actors/${id}'

{
    "deleted_actor": "Actor with id: 12",
    "success": true
}

GET '/api/v1.0/movies'

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

        '''
    ],
    "success": true
}


GET '/api/v1.0/movies/${id}'

{
    "movie": {
        "id": 1,
        "release_date": "Mon, 12 Jun 2023 00:00:00 GMT",
        "title": "A Broken Rose"
    },
    "featured_actors": [
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


POST ...
DELETE ...

