from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .database.models import db_drop_and_create_all, setup_db
from .auth.auth import AuthError
from .views import drinks

load_dotenv()
app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

# ROUTES
app.register_blueprint(drinks)

# Error Handling
'''
Error handling for bad request.
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    'success': False,
                    'error': 400,
                    'message': 'bad request'
                    }), 400


'''
Error handling for resource not found.
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    'success': False,
                    'error': 404,
                    'message': 'resource not found'
                    }), 404


'''
Error handling for method not allowed.
'''
@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
                    'success': False,
                    'error': 405,
                    'message': 'method not allowed'
                    }), 405


'''
Error handling for unprocessable entity.
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    'success': False,
                    'error': 422,
                    'message': 'unprocessable'
                    }), 422


'''
Error handling for internal server error.
'''
@app.errorhandler(500)
def server_error(error):
    return jsonify({
                    'success': False,
                    'error': 500,
                    'message': 'internal server error'
                    }), 500


'''
Error handling for service unavailable errors
for instance database connection errors.
'''
@app.errorhandler(503)
def service_unavailable(error):
    return jsonify({
                    'success': False,
                    'error': 503,
                    'message': 'service unavailable'
                    }), 503


'''
Error handling for Authentication errors.
Returns 401, 403 or 400 error codes.
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    'success': False,
                    'error': error.status_code,
                    'message': error.error['description']
                    }), error.status_code