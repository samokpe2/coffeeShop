import json
from flask import Blueprint, abort, jsonify, request
from sqlalchemy import exc

from .database.models import Drink
from .auth.auth import requires_auth
from .helpers import (
    validate_create_drink_request,
    validate_recipe_body,
    isValidTitle
)


drinks = Blueprint('drinks', __name__)

'''
Retrieves an undetailed list of drinks.
'''
@drinks.route('/drinks', methods=['GET'])
def retrieve_drinks():
    try:
        data = Drink.query.all()
        if not data:
            abort(404)
        drinks = [drink.short() for drink in data]
        return jsonify({
                    'success': True,
                    'drinks': drinks
                }), 200
    except exc.SQLAlchemyError:
        abort(503)


'''
Retrieves a detailed list of drinks.
'''
@drinks.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail():
    try:
        data = Drink.query.all()
        if not data:
            abort(404)
        drinks = [drink.long() for drink in data]
        return jsonify({
                    'success': True,
                    'drinks': drinks
                }), 200
    except exc.SQLAlchemyError:
        abort(503)


'''
Creates a new drink.
'''
@drinks.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    validate_create_drink_request(request)
    try:
        recipe = json.loads(request.data)['recipe']
        drink = Drink(
            title=json.loads(request.data)['title'],
            recipe=json.dumps(recipe)
        )
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200
    except exc.SQLAlchemyError as e:
        print(e)
        abort(422)
    except Exception:
        abort(503)


'''
Edits a drink's details.
'''
@drinks.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink_details(id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            abort(404)
        for item in json.loads(request.data).keys():
            if item == 'title' and isValidTitle(request):
                title = json.loads(request.data)['title']
                drink.title = title
            elif item == 'recipe':
                validate_recipe_body(request)
                recipe = json.loads(request.data)['recipe']
                drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except exc.SQLAlchemyError:
        abort(422)


'''
Deletes a drink.
'''
@drinks.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            abort(404)
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except exc.SQLAlchemyError:
        abort(503)