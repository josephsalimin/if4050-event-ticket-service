from flask import Blueprint, jsonify, request
from .controller import *


# Blue print for Auth
auth = Blueprint("auth_controller", __name__, template_folder="templates")


@auth.route("/create", methods=["POST"])
def create():
    username = request.json.get("name", "").strip().lower()
    auth_type = request.json.get("type", "").strip().lower()
    partner_id = request.json.get("partner_id", 0)
    if username == "" or auth_type == "":
        raise ApplicationException("Input error")
    return jsonify(create_auth_service(username, auth_type, partner_id))


@auth.route("/refresh", methods=["POST"])
def update():
    name = request.json.get("name", "").strip()
    refresh_token = request.json.get("refresh_token", "").strip()
    if name == "" or refresh_token == "":
        raise ApplicationException("Input error")
    return jsonify(refresh_auth_token(name, refresh_token))


@auth.route("/verify", methods=["POST"])
def verify():
    auth_token = request.json.get("auth_token", "").strip()
    if auth_token == "":
        raise ApplicationException("Input error")
    return jsonify(verify_auth(auth_token))


@auth.route("/<auth_id>", methods=["GET"])
def read(auth_id):
    return jsonify(get_auth(auth_id))