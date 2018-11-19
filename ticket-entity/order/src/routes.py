from flask import Blueprint, request, jsonify
from .controller import *


order = Blueprint("order_controller", __name__, template_folder="templates")


@order.route("/", methods=["POST"])
@order.route("", methods=["POST"])
def create():
    body = request.json
    try:
        user_id = body["user_id"]
        total_price = body["total_price"]
        list_ticket_section = body["section_list"]
        return jsonify(create_order(user_id, total_price, list_ticket_section))
    except KeyError:
        raise ApplicationException("Wrong input")


@order.route("/<order_id>", methods=["PUT"])
def pay(order_id):
    return jsonify(pay_order(order_id))


@order.route("/<order_id>", methods=["DELETE"])
def cancel(order_id):
    return jsonify(cancel_order(order_id))


@order.route("/<order_id>", methods=["GET"])
def read(order_id):
    return jsonify(get_order(order_id))


@order.route("/user", methods=["GET"])
def read_by_user():
    user_id = request.args.get("id", 0)
    return jsonify(get_order_by_user(user_id))