import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, endpoint_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
NOTE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()
##############################ENDPOINTS##################################

@app.route('/drinks', methods = ['GET'])
def get_drink():
    try:
        drinks = Drink.query.all()
        data = [drink.short() for drink in drinks]
        return jsonify({
            "success" : "True",
            "drinks": data
        })
    except:
        abort(400)

@app.route('/drinks-detail', methods = ['GET'])
#@endpoint_auth('get:drinks-detail')
def get_drink_details():
    try:
        drinks = Drink.query.all()
        data = [drink.long() for drink in drinks]
        return jsonify({
            "success" : "True",
            "drinks": data
        })
    except:
        abort(400)

@app.route('/drinks', methods = ['POST'])
@endpoint_auth('post:drinks')
def create_drink():
    try:
        data_body = request.get_json()
        new_title = data_body.get("title",'')
        new_recipe = data_body.get("recipe", None)
        exist_drink = Drink.query.filter(Drink.title == new_title).one_or_none()
        if new_title is '':
            abort(400)
        else:
            if exist_drink is None:
                new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
                new_drink.insert()
            else:
                abort(400)
        drinks = Drink.query.all()
        data = [drink.long() for drink in drinks]
        return jsonify({
            "success" : "True",
            "drinks" :data
        })
    except:
        abort(422)    
    
@app.route('/drinks/<int:drink_id>', methods = ['PATCH'])
@endpoint_auth('patch:drinks')
def update_drinks(drink_id):
    data_body = request.get_json()
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    if "title" in data_body:
        update_title = data_body.get("title", None)
        drink.title = update_title
    if "recipe" in data_body:
        update_recipe = data_body.get("recipe",None)
        drink.recipe = json.dumps(update_recipe)

    #drink.title = update_title
    #drink.recipe = json.dumps(update_recipe)
    drink.update()
    drinks = Drink.query.all()
    data = [drink.long() for drink in drinks]
    return jsonify({
            "success": True,
            "drinks":data
         })

@app.route('/drinks/<int:drink_id>', methods = ['DELETE'])
@endpoint_auth('delete:drinks')
def delete_drinks(drink_id):
    
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    else:
        drink.delete()
    return jsonify({
            "success": True,
            "deleted": drink.id,
        })
     
########Error Handling################

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
       "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
       "message": "Resource Not Found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
       "message": "Bad Request"
    }), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "internal server error"
        }),500


@app.errorhandler(AuthError)
def un_authorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Unauthorized"
        }),401

@app.errorhandler(AuthError)
def forbidden_authorization(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "Forbidden"
        }),403