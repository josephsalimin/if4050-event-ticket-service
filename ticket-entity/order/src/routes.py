from flask import Blueprint, request, jsonify
from .controller import *


order = Blueprint("order_controller", __name__, template_folder="templates")


@order.route("", methods=["POST"])
@order.route("/", methods=["POST"])
def create():
    body = request.json
    try:
        user_id = body["user_id"]
        total_price = body["total_price"]
    except KeyError:
        raise ApplicationException("Input error")
    return jsonify(create_order(user_id, total_price))


@order.route("/<order_id>", methods=["PUT"])
def pay(order_id):
    return jsonify(pay_order(order_id))


@order.route("/<order_id>", methods=["DELETE"])
def cancel(order_id):
    return jsonify(cancel_order(order_id))


@order.route("/<order_id>", methods=["GET"])
def read(order_id):
    return jsonify(get_order(order_id))