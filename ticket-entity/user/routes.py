from flask import Blueprint, jsonify, g
from .controller import *
from flask import request
from .exception import ApplicationException
from .database import DatabaseManager
import requests
import os


user = Blueprint("user_controller", __name__, template_folder="templates")


@user.before_request
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
    g.company_id = r.json()["id"]
    # Connect database
    DatabaseManager.get_database().connect()


@user.after_request
def after_request(response):
    DatabaseManager.get_database().close()
    return response


@user.errorhandler(ApplicationException)
def error_auth_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


@user.route("/", methods=["POST"])
@user.route("", methods=["POST"])
def create():
    body = request.json
    try:
        username = body["username"]
        fullname = body["fullname"]
        email = body["email"]
        password = body["password"]
        address = body["address"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(create_user(g.company_id, username, fullname, email, password, address))


@user.route("/", methods=["GET"])
@user.route("", methods=["GET"])
def search():
    username = request.args.get("username", "")
    email = request.args.get("email", "")
    return jsonify(search_user(g.company_id, username, email))


@user.route("/<user_id>", methods=["GET"])
def read(user_id):
    return jsonify(get_user_detail(g.company_id, user_id))


@user.route("/<user_id>", methods=["PUT"])
def update(user_id):
    body = request.json
    try:
        fullname = body["fullname"]
        address = body["address"]
    except KeyError:
        raise ApplicationException("Input error")
    return jsonify(update_user(g.company_id, user_id, fullname, address))
