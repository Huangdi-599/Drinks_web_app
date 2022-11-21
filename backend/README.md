# Backend REST API

## Descriptions






## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

When using Python for projects, we advise working in a virtual setting. This keeps the dependencies you have for each project tidy and distinct. The link contains details on how to set up a virtual environment for your platform.
[python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Install dependencies by going to the `/backend` directory and performing the following commands after your virtual environment is up and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./backend/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the API directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Setting up your Database

- From the `/backend/database` directory, navigate to the `models.py` file to examine the database name and location. This API contains a SQLite database server,you can also configure your preferred database.
- To remove any existing databases and generate new ones once the server begins, uncomment `db drop and create all()` on the `app.py` file in the `/backend` directory.


## Endpoints Documentation
`GET '/drinks'`
- brings up a list of beverages that are available, where the "id," "receipe," and "title" components are equivalent to their values and the "recipe" element has a brief dictionary with the key; Values of "color" ,"parts"
- Request Arguments: None
- Returns: An object with a single key, `drinks`, that contains an object of `id`,`recipe`,`title` key: value pairs.

```json
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": "True"
}
```

`GET '/drinks-detail'`
- brings up a list of beverages that are available, where the "id," "receipe," and "title" components are equivalent to their values and the "recipe" element has a brief dictionary with the key; Values of "color," "parts," and "name", This endpoint requires an authorization of (get:drinks-details) from JWT
- Request Arguments: None
- Returns: An array with a single key, `drinks`, that contains an object of `id`,`recipe`,`title` key: value pairs.

```json
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": "True"
}
```
`POST '/drinks'`
- brings up a list of beverages that are available, where the "id," "receipe," and "title" components are equivalent to their values and the "recipe" element has a brief dictionary with the key; Values of "color," "parts," and "name", This endpoint requires an authorization of (get:drinks-details) from JWT
- Request Arguments: None
- Returns: An array with a single key, `drinks`, that contains an object of `id`,`recipe`,`title` key: value pairs.

```json
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": "True"
}
```


## Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 500,
    "message": "Internal Server Error"
}
```
The API will return six error types when requests fail:
400: Bad Request
401: Unauthorized
403: Forbidden
404: Resource Not Found
422: Not Processable
500: Internal Server Error