from .exception import ApplicationException
from .models import Order, ReservedTicket


def create_order(user_id, total_price, auth_id, list_ticket_section):
    """
    Function to create order
    :param auth_id: int
    :param user_id: int
    :param total_price: int
    :param list_ticket_section: array of dict
    :return: dict
    """
    order = Order(user_id=user_id, total_price=total_price, auth_id=auth_id, status="pending")
    list_reserved = []
    for section_ticket in list_ticket_section:
        reserved = ReservedTicket(section_id=section_ticket["id"], quantity=section_ticket["quantity"], order=order)
        list_reserved.append(reserved)
    order.save()
    for reserved in list_reserved:
        reserved.save()
    return order.to_dict()


def pay_order(order_id, auth_id):
    """
    Function to pay order from order_id
    :param auth_id: int
    :param order_id: int
    :return: array of dict
    """
    order = Order.get_or_none(Order.id == order_id, Order.auth_id == auth_id)
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


def cancel_order(order_id, auth_id):
    """
    Function to cancel order from order_id
    :param auth_id: auth_id
    :param order_id: int
    :return: array of dict
    """
    order = Order.get_or_none(Order.id == order_id, Order.auth_id == auth_id)
    if order is None:
        raise ApplicationException("Order not found")
    if order.status == "cancelled":
        return []
    order.status = "cancelled"
    list_reserved = ReservedTicket.select().where(ReservedTicket.order == order)
    section_list = [{
        "id": reserved.section_id,
        "quantity": reserved.quantity 
    } for reserved in list_reserved]
    order.save()
    return section_list


def get_order(order_id, auth_id):
    """
    Function to get order detail from order_id
    :param auth_id: int
    :param order_id: int
    :return: dict
    """
    order = Order.get_or_none(Order.id == order_id, Order.auth_id == auth_id)
    if order is None:
        raise ApplicationException("Order not found")
    list_reserved = ReservedTicket.select().where(ReservedTicket.order == order)
    resp = order.to_dict()
    resp["section_list"] = [reserved.to_dict() for reserved in list_reserved]
    return resp


def get_order_by_user(user_id, auth_id):
    """
    Function to get order from user
    :param auth_id: int
    :param user_id: int
    :return: array of dict
    """
    orders = Order.select().where(Order.user_id == user_id, Order.auth_id == auth_id)
    resp = [order.to_dict() for order in orders]
    return resp
