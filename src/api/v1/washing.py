# import modules, models and configs
from datetime import datetime, timedelta
import re

import jwt
from flask import jsonify, request, abort
# jsonify converts objects to JSON strings
# abort method either accepts an error code or it can accept a Response object

from api.__init__ import app, databases
from api.v1.models import Washing
from flask import render_template

databases.create_all()

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''

'''
    (UTF) Unicode Transformation Format
    its a character encoding
    A character in UTF8 can be from 1 to 4 bytes long
    UTF-8 is backwards compatible with ASCII
    is the preferred encoding for e-mail and web pages
'''


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'The request can not be linked to, Please check your endpoint url'})
    response.status_code = 404
    return response


# 405 error handler
@app.errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'Invalid request method. Please check the request method being used'})
    response.status_code = 405
    return response


# 401 error handler
@app.errorhandler(401)
def internal_server_error(e):
    response = jsonify({"error": "Token is invalid"})
    response.status_code = 401
    return response


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'Error, Server currently down, please restart the server to use the bucketlist API'})
    response.status_code = 500
    return response


@app.route('/')
def homepage():
    """ The homepage route
    :return: A welcome message
    """
    return render_template('index.html')

# add washing type method
@app.route('/washing/api/v1/washingtypes', methods=['POST'])
def add_washing_method():
    request.get_json(force=True)
    # try:
    #     verification = verify_token(request)
    #     if isinstance(verification, dict):
    #         user_id = verification['user_id']
    #     else:
    #         return verification

        w_name = request.json['name']
        w_price = request.json['price']
        w_description = request.json['description']
        if not w_name:
            response = jsonify({'Error': 'washing package has no name'})
            response.status_code = 400
            return response
        if not w_price:
            response = jsonify({'Error': 'washing package has no price tag'})
            response.status_code = 400
            return response
        if not w_description:
            response = jsonify({'Error': 'washing package has no description'})
            response.status_code = 400
            return response

        res = Washing.query.all()
        data_check = [data for data in res if data.name == w_name]
        if data_check:
            response = jsonify({'Warning': 'this washing package already exists.'})
            response.status_code = 409
            return response
        else:
            w = Washing(name=w_name, price=w.price, description=w.description)
            w.save()
            response = jsonify({'status': 'Washing package added successfully'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({'Error': 'Use the name for dict key.'})
        response.status_code = 500
        return response


# get bucket method
@app.route('/washing/api/v1/washingtypes', methods=['GET'])
def retrieve_washing_method():
    message = 'No washing packages have been added yet'
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload

    limit = int(request.args.get("limit", 3))
    if limit > 100:
        limit = 100
    respons = Washing.query.all()
    if not respons:
        response = jsonify({'error': 'No washing package has been created yet'})
        response.status_code = 200
        return response
    else:
        search = request.args.get("q", "")
        if search:
            res = [wash for wash in respons if wash.name in search]
            if not res:
                response = jsonify({'error': 'The washing package you searched does not exist'})
                return response
            else:
                washing_data = []
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                    }
                    washing_data.clear()
                    washing_data.append(final)
                response = jsonify(washing_data)
                response.status_code = 200
                return response
        else:
            res = [wash for wash in respons]
            washing_data = []
            if not res:
                response = jsonify({'error': message})
                response.status_code = 200
                return response
            else:
                for data in res:
                    final = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified,
                    }
                    washing_data.append(final)
                response = jsonify(washing_data)
                response.status_code = 200
                return response


# get, update and delete washing package
@app.route('/washing/api/v1/washingtypes/<int:washing_id>', methods=['GET', 'PUT', 'DELETE'])
def washing_by_id(washing_id):
    # payload = verify_token(request)
    # if isinstance(payload, dict):
    #     user_id = payload['user_id']
    # else:
    #     return payload
    res = Washing.query.all()
    washing_data = [wash for wash in res if wash.id == wash_id]
    if request.method == 'GET':
        data = {}
        for data in washing_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if washing_id not in data.values():
            response = jsonify({'warning': 'the washing package does not exist.'})
            response.status_code = 404
            return response
        else:
            response = jsonify(data)
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        data = {}
        for data in washing_data:
            data = {
                'id': data.id,
                'name': data.name,
                'price': data.price,
                'description': data.description,
                'date-created': data.date_created,
                'date_modified': data.date_modified,
            }
        if washing_id not in data.values():
            response = jsonify({'warning': 'the washing package does not exist.'})
            response.status_code = 404
            return response
        else:
            delete = Washing.query.filter_by(id=washing_id).first()
            databases.session.delete(delete)
            databases.session.commit()
            response = jsonify({'Status': 'Washing package deleted successfully.'})
            response.status_code = 200
            return response
    elif request.method == 'PUT':
        request.get_json(force=True)
        data = Washing.query.filter_by(id=washing_id).first()
        if not data:
            response = jsonify({'warning': 'the Washing package does not exist.'})
            response.status_code = 404
            return response
        else:
            try:
                name = request.json['name']
                data.name = name
                databases.session.commit()
                data = {}
                for data in bucket_data:
                    data = {
                        'id': data.id,
                        'name': data.name,
                        'price': data.price,
                        'description': data.description,
                        'date-created': data.date_created,
                        'date_modified': data.date_modified
                    }
                response = jsonify(data)
                response.status_code = 201
                return response
            except KeyError:
                response = jsonify({'error': 'Please use name for dict keys.'})
                response.status_code = 500
                return response