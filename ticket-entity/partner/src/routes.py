from flask import Blueprint, jsonify, g, request
from .controller import *
from app_exception import ApplicationException


partner = Blueprint("partner_controller", __name__, template_folder="templates")


@partner.route("/", methods=["POST"])
@partner.route("", methods=["POST"])
def create():
    body = request.json
    try:
        name = body["name"]
        address = body["address"]
        email = body["email"]
        contact_number = body["contact_number"]
    except:
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
    except:
        raise ApplicationException("Input error")
    return jsonify(update_partner(partner_id, name, address, email, contact_number))


@partner.route("/", methods=["GET"])
@partner.route("", methods=["GET"])
def read_list_partner():
    name = request.args.get("name", None).lower()
    if name is None or name == "":
        raise ApplicationException("Input error")
    return jsonify(get_list_partner(name))
