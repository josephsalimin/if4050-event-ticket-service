from flask import Blueprint, request, jsonify, g
from .controller import *
from .exception import ApplicationException
from .database import DatabaseManager
import requests
import os


order = Blueprint("order_controller", __name__, template_folder="templates")


@order.before_request
def before_request():
    # Validate request method and type
    if request.method != 'GET' and not request.is_json:
        raise ApplicationException("Must be JSON type")
    # Validate for Authorization
    jwt_token = request.headers.get('Authorization')
    if jwt_token is None:
        raise ApplicationException("Not authorized")
    r = requests.post(os.environ.get("AUTH_URL"), json={"auth_token": jwt_token})
    if r.status_code != 200 or not r.json()["valid"]:
        raise ApplicationException("Not authorized")
    auth = r.json()
    g.jwt_token = jwt_token
    g.auth_id = auth["id"]
    g.auth_type = auth["auth_type"]
    # Connect database
    DatabaseManager.get_database().connect()


@order.after_request
def after_request(response):
    DatabaseManager.get_database().close()
    return response


@order.errorhandler(ApplicationException)
def error_auth_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


@order.route("/", methods=["POST"])
@order.route("", methods=["POST"])
def create():
    body = request.json
    try:
        user_id = body["user_id"]
        total_price = body["total_price"]
        list_ticket_section = body["section_list"]
        return jsonify(create_order(user_id, total_price, g.auth_id, list_ticket_section))
    except KeyError:
        raise ApplicationException("Wrong input")


@order.route("/<order_id>", methods=["PUT"])
def pay(order_id):
    return jsonify(pay_order(order_id, g.auth_id))


@order.route("/<order_id>", methods=["DELETE"])
def cancel(order_id):
    return jsonify(cancel_order(order_id, g.auth_id))


@order.route("/<order_id>", methods=["GET"])
def read(order_id):
    return jsonify(get_order(order_id, g.auth_id))


@order.route("/user", methods=["GET"])
def read_by_user():
    user_id = request.args.get("id", 0)
    return jsonify(get_order_by_user(user_id, g.auth_id))
