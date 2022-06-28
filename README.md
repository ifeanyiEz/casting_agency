# Casting Agency API

## Running Locally

In order to successfully run the project on your local server, you'd need to pay attention to the following:

#### Install Dependencies

#### App Local Run
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```
#### Test_App Local Run 
```
dropdb casting_test && createdb casting_test
psql casting_test < casting_test.psql
python3 test_app.py
```

#### Endpoints:

##### GET '/api/v1.0/actors'

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


##### GET '/api/v1.0/actors/${id}'

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
