import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from os.path import join, dirname
from app_exception import ApplicationException
from src.database import DatabaseManager


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from src.routes import auth

# Creating Flask App
app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/auth")


@app.before_request
def before_request():
    DatabaseManager.get_database().connect()
    if request.method != 'GET' and not request.is_json:
        raise ApplicationException("Must be JSON type")


@app.after_request
def after_request(response):
    DatabaseManager.get_database().close()
    return response


@app.errorhandler(ApplicationException)
def error_auth_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


if __name__ == '__main__':
    app.run(port=os.environ.get('AUTH_PORT'), debug=True)
