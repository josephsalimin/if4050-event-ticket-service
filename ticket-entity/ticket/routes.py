from flask import Blueprint, request, jsonify, g
import requests
import os
from .database import DatabaseManager
from .controller import *
from .exception import ApplicationException
from functools import wraps


ticket_section = Blueprint("ticket_section_controller", __name__, template_folder="templates")
ticket = Blueprint("ticket_controller", __name__, template_folder="templates")


def auth_partner(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):
        if g.auth_type != "partner" and g.auth_type != "master":
            raise ApplicationException("Only Partner can access this API")
        return callback()
    return wrapper


def handle_before_request():
    # Validate request method and type
    if (request.method != 'GET' and request.method != 'DELETE') and not request.is_json:
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
    g.partner_id = auth["partner_id"]
    g.auth_type = auth["auth_type"]
    # Connect database
    DatabaseManager.get_database().connect()


def handle_after_request(response):
    DatabaseManager.get_database().close()
    return response


@ticket_section.before_request
def before_request():
    handle_before_request()


@ticket_section.after_request
def after_request(response):
    return handle_after_request(response)


@ticket_section.errorhandler(ApplicationException)
def error_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


@ticket.before_request
def before_request():
    handle_before_request()


@ticket.after_request
def after_request(response):
    return handle_after_request(response)


@ticket.errorhandler(ApplicationException)
def error_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


@ticket_section.route("/", methods=["POST"])
@ticket_section.route("", methods=["POST"])
@auth_partner
def issue_ticket_from_event():
    body = request.json
    try:
        event_id = body["event_id"]
        list_ticket_section = body["section_list"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(issue_ticket(event_id, list_ticket_section))


@ticket_section.route("/event", methods=["GET"])
def read_by_event():
    event_id = request.args.get("id", 0)
    if event_id == 0:
        return jsonify([])
    return jsonify(get_section_by_event(event_id))


@ticket_section.route("/validation", methods=["POST"])
def validate():
    try:
        list_ticket_section = request.json["section_list"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(validate_ticket_section(list_ticket_section))


@ticket_section.route("/<int:section_id>", methods=["GET"])
def read_section(section_id):
    return jsonify(get_section_detail(section_id))


@ticket_section.route("/capacity_reduce", methods=["POST"])
def reduce_capacity():
    try:
        list_ticket_section = request.json["section_list"]
        return jsonify(change_section_capacity(list_ticket_section, 'reduce'))
    except KeyError:
        raise ApplicationException("Wrong input")


@ticket_section.route("/capacity_add", methods=["POST"])
def add_capacity():
    try:
        list_ticket_section = request.json["section_list"]
        return jsonify(change_section_capacity(list_ticket_section, 'add'))
    except KeyError:
        raise ApplicationException("Wrong input")


@ticket.route("/", methods=["POST"])
@ticket.route("", methods=["POST"])
def generate_ticket_from_order():
    body = request.json
    try:
        order_id = body["order_id"]
        list_ticket_section = body["section_list"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(generate_ticket(order_id, list_ticket_section))


@ticket.route("/", methods=["DELETE"])
@ticket.route("", methods=["DELETE"])
def remove_ticket_from_order():
    body = request.json
    try:
        order_id = body["order_id"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(remove_ticket(order_id))


@ticket.route("/<int:ticket_id>", methods=["GET"])
def read_ticket(ticket_id):
    return jsonify(get_ticket_detail(ticket_id))


@ticket.route("/order", methods=["GET"])
def read_by_order():
    order_id = request.args.get("id", 0)
    return jsonify(get_ticket_by_order(order_id))
