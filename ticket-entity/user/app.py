import os
from flask import Flask, request, jsonify, g
from dotenv import load_dotenv
from os.path import join, dirname
from app_exception import ApplicationException
from src.database import DatabaseManager
import requests


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from src.routes import user

# Creating Flask App
app = Flask(__name__)
app.register_blueprint(user, url_prefix="/user")


@app.before_request
def before_request():
    # Validate request: method, type, header
    if request.method != 'GET' and not request.is_json:
        raise ApplicationException("Must be JSON type")
    auth = request.headers.get('Authorization')
    if auth is None:
        raise ApplicationException("Not authorized")
    r = requests.post(os.environ.get("AUTH_URL"), json={"auth_token": auth})
    if r.status_code != 200 or not r.json()["valid"]:
        raise ApplicationException("Not authorized")
    print(r.json())
    g.company_id = r.json()["id"]
    # Connect database
    DatabaseManager.get_database().connect()


@app.after_request
def after_request(response):
    DatabaseManager.get_database().close()
    return response


@app.errorhandler(ApplicationException)
def error_auth_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


if __name__ == '__main__':
    app.run(port=os.environ.get('USER_PORT'), debug=True)
