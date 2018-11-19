from flask import Blueprint, jsonify, g
from .controller import *
from flask import request


user = Blueprint("user_controller", __name__, template_folder="templates")


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
        raise ApplicationException("Input error")
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