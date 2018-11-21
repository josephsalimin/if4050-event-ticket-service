from flask import Blueprint, request, jsonify, g
from .controller import *
from .exception import ApplicationException
from .models import DatabaseManager
from functools import wraps
import requests, os


event = Blueprint("event_controller", __name__, template_folder="templates")


@event.before_request
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
    auth = r.json()
    g.partner_id = auth["partner_id"]
    g.auth_type = auth["auth_type"]
    # Connect database
    DatabaseManager.get_database().connect()


@event.after_request
def after_request(response):
    DatabaseManager.get_database().close()
    return response


@event.errorhandler(ApplicationException)
def error_auth_exception(error):
    payload = {"message": str(error)}
    return jsonify(payload), error.status_code


def auth_partner(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.auth_type != "partner" and g.auth_type != "master":
            raise ApplicationException("Only Partner can access this API")
        return f(*args, **kwargs)
    return wrapper


@event.route("/", methods=["POST"])
@event.route("", methods=["POST"])
@auth_partner
def create():
    body = request.json
    try:
        partner_id = body["partner_id"]
        name = body["name"]
        description = body.get("description", "-")
        location = body["location"]
        start_at = body["start_at"]
        end_at = body["end_at"]
    except KeyError:
        raise ApplicationException("Input error")
    return jsonify(create_event(partner_id, name, description, location, start_at, end_at))


@event.route("/<event_id>", methods=["PUT"])
@auth_partner
def update(event_id):
    body = request.json
    try:
        name = body["name"]
        description = body.get("description", "")
        location = body["location"]
        start_at = body["start_at"]
        end_at = body["end_at"]
    except KeyError:
        raise ApplicationException("Input error")
    return jsonify(update_event(event_id, g.partner_id, name, description, location, start_at, end_at))


@event.route("/<event_id>", methods=["GET"])
def read(event_id):
    return jsonify(get_event_detail(event_id))


@event.route("/history", methods=["GET"])
def read_by_history():
    return jsonify(get_list_event_history())


@event.route("/available", methods=["GET"])
def read_by_availability():
    return jsonify(get_list_event_available())


@event.route("/partner", methods=["GET"])
def get_by_partner():
    partner_id = request.args.get("id", 0)
    return jsonify(get_events_by_partner(partner_id))