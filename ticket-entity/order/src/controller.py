from app_exception import ApplicationException
from .models import Order, ReservedTicket
import os
import requests


def create_order(user_id, total_price):
    order = Order(user_id=user_id, total_price=total_price, status="pending")
    order.save()
    return order.to_dict()


def pay_order(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if order is None:
        raise ApplicationException("Order not found")
    if order.status == "cancelled":
        raise ApplicationException("Order already cancelled")
    order.status = "paid"
    reserveds = ReservedTicket.select().where(ReservedTicket.order_id == order_id)
    section_list = [{
        "id": reserved.section_id,
        "quantity": reserved.quantity 
    } for reserved in reserveds]
    order.save()
    return section_list


def cancel_order(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if order is None:
        raise ApplicationException("Order not found")
    if order.status == "cancelled":
        raise ApplicationException("Order already cancelled")
    order.status = "cancelled"
    reserveds = ReservedTicket.select().where(ReservedTicket.order_id == order_id)
    section_list = [{
        "id": reserved.section_id,
        "quantity": reserved.quantity 
    } for reserved in reserveds]
    order.save()
    return section_list


def get_order(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if order is None:
        raise ApplicationException("Order not found")
    return order.to_dict()