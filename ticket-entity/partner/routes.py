import requests
import os
from flask import Blueprint, jsonify, request
from .controller import *
from .exception import ApplicationException
from .models import DatabaseManager


partner = Blueprint("partner_controller", __name__, template_folder="templates")


@partner.before_request
def before_request():
    # Validate request method and type
    if request.method != 'GET' and not request.is_json:
        raise ApplicationException("Must be JSON type")
    # Validate for Authorization
    auth = request.headers.get('Authorization')
    if auth is None:
        raise ApplicationException("Not authorized")
    r = requests.post(os.environ.get("AUTH_URL"), json={"auth_token": auth})
    if r.status_code != 200 or not r.json()["valid"]:
        raise ApplicationException("Not authorized")
    auth_id = r.json()["id"]
    if int(auth_id) != 1:
        raise ApplicationException("Only TicketX can access this API")
    # Connect database
    DatabaseManager.get_database().connect()


@partner.after_request
def after_request(response):
    DatabaseManager.get_database().close()
    return response


@partner.errorhandler(ApplicationException)
def error_auth_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


@partner.route("/", methods=["POST"])
@partner.route("", methods=["POST"])
def create():
    body = request.json
    try:
        name = body["name"]
        address = body["address"]
        email = body["email"]
        contact_number = body["contact_number"]
    except KeyError:
        raise ApplicationException("Input error")
    return jsonify(create_partner(name, address, email, contact_number))


@partner.route("/<partner_id>", methods=["GET"])
def read(partner_id):
    return jsonify(get_partner_detail(partner_id))


@partner.route("/<partner_id>", methods=["PUT"])
def update(partner_id):
    body = request.json
    try:
        name = body["name"]
        address = body["address"]
        email = body["email"]
        contact_number = body["contact_number"]
    except KeyError:
        raise ApplicationException("Input error")
    return jsonify(update_partner(partner_id, name, address, email, contact_number))


@partner.route("/", methods=["GET"])
@partner.route("", methods=["GET"])
def read_list_partner():
    return jsonify(get_list_partner())
