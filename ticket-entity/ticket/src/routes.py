from flask import Blueprint, request, jsonify
from .controller import *


ticket_section = Blueprint("ticket_section_controller", __name__, template_folder="templates")
ticket = Blueprint("ticket_controller", __name__, template_folder="templates")


def auth_partner(callback):
    def wrapper(*args, **kwargs):
        if g.auth_type != "partner" and g.auth_type != "master":
            raise ApplicationException("Only Partner can access this API")
        return callback()
    return wrapper


@ticket_section.route("/", methods=["POST"])
@ticket_section.route("", methods=["POST"])
@auth_partner
def issue_ticket_from_event():
    body = request.json
    print(body)
    try:
        event_id = body["event_id"]
        list_ticket_section = body["section_list"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(issue_ticket(event_id, list_ticket_section))


@ticket_section.route("/event", methods=["GET"])
def read_by_event():
    event_id = request.args.get("id", 0)
    return jsonify(get_section_by_event(event_id))


@ticket_section.route("/validation", methods=["POST"])
def validate():
    try:
        list_ticket_section = request.json["section_list"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return validate_ticket_section(list_ticket_section)


@ticket_section.route("/<section_id>", methods=["GET"])
def read_section(section_id):
    return jsonify(get_section_detail(section_id))


@ticket_section.route("/reduce", methods=["POST"])
def reduce_quantity():
    try:
        list_ticket_section = request.json["section_list"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return reduce_section_quantity(list_ticket_section)


@ticket_section.route("/add", methods=["POST"])
def add_quantity():
    try:
        list_ticket_section = request.json["section_list"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return add_section_quantity(list_ticket_section)


@ticket.route("/", methods=["POST"])
def generate_ticket_from_order():
    body = request.json
    try:
        order_id = body["order_id"]
        list_ticket_section = body["list_ticket_section"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(generate_ticket(order_id, list_ticket_section))


@ticket.route("/remove", methods=["DELETE"])
def remove_ticket_from_order():
    body = request.json
    try:
        order_id = body["order_id"]
    except KeyError:
        raise ApplicationException("Wrong input")
    return jsonify(generate_ticket(order_id))


@ticket.route("/<ticket_id>", methods=["GET"])
def read_ticket(ticket_id):
    return jsonify(get_ticket_detail(ticket_id))


@ticket.route("/order", methods=["GET"])
def read_by_order():
    order_id = request.args.get("id", 0)
    return jsonify(get_section_by_event(order_id))