from flask import Blueprint, jsonify, request, g
from .controller import *
from .database import DatabaseManager
from .exception import ApplicationException


# Blue print for Auth
auth = Blueprint("auth_controller", __name__, template_folder="templates")


@auth.before_request
def before_request():
    DatabaseManager.get_database().connect()
    if request.method != 'GET' and not request.is_json:
        raise ApplicationException("Must be JSON type")
    g.jwt = request.headers.get('Authorization', None)


@auth.after_request
def after_request(response):
    DatabaseManager.get_database().close()
    return response


@auth.errorhandler(ApplicationException)
def error_auth_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


def check_master_auth(callback):
    def wrapper(*args, **kwargs):
        if g.jwt is None:
            raise ApplicationException("Must add header", 401)
        decode = jwt.decode(g.jwt, os.environ.get("REFRESH_KEY"), algorithms='HS256')
        auth_type = decode.get("auth_type", 0)
        if auth_type != "master":
            raise ApplicationException("Only TicketX can access this API", 401)
        return callback(*args, **kwargs)
    return wrapper()


@auth.route("/create", methods=["POST"])
@check_master_auth
def create():
    username = request.json.get("name", "").strip().lower()
    auth_type = request.json.get("type", "").strip().lower()
    partner_id = request.json.get("partner_id", 0)
    if username == "" or auth_type == "":
        raise ApplicationException("Input error")
    return jsonify(create_auth_service(username, auth_type, partner_id))


@auth.route("/refresh", methods=["POST"])
@check_master_auth
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
    print(auth_id)
    return jsonify(get_auth(auth_id))
