from app_exception import ApplicationException
from .models import Order, ReservedTicket
import os
import requests


def create_order(user_id, total_price, list_ticket_section):
    order = Order(user_id=user_id, total_price=total_price, status="pending")
    reserveds = []
    for section_ticket in list_ticket_section:
        reserved = ReservedTicket(section_id=section_ticket["id"], quantity=section_ticket["quantity"], order=order)
        reserveds.append(reserved)
    order.save()
    for reserved in reserveds:
        reserved.save()
    return order.to_dict()


def pay_order(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if order is None:
        raise ApplicationException("Order not found")
    if order.status == "cancelled" or order.status == "paid":
        return []
    order.status = "paid"
    reserveds = ReservedTicket.select().where(ReservedTicket.order == order)
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
        return []
    order.status = "cancelled"
    reserveds = ReservedTicket.select().where(ReservedTicket.order == order)
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
    reserveds = ReservedTicket.select().where(ReservedTicket.order == order)
    resp = order.to_dict()
    resp["section_list"] = [reserved.to_dict() for reserved in reserveds]
    return resp


def get_order_by_user(user_id):
    orders = order.select().where(Order.user_id == user_id)
    resp = [order.to_dict() for order in orders]
    return resp