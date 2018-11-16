from flask import g
from app_exception import ApplicationException
from .models import Ticket, Section, DoesNotExist, IntegrityError
import requests
import os


def issue_ticket(event_id, list_ticket_section):
    sections = []
    for ticket_section in list_ticket_section:
        try:
            name, price = ticket_section["name"], ticket_section["price"]
            capacity, has_seat = ticket_section["capacity"], ticket_section["has_seat"]
        except KeyError:
            raise ApplicationException("Input error", 400)
        sections += create_ticket_section(has_seat, event_id, name, price, capacity)
    for section in sections:
        section.save()
    return True


def create_ticket_section(has_seat, event_id, name, price, capacity):
    sections = []
    if has_seat:
        for i in range(capacity):
            section = Section(
                name=(name + str(i)), max_capacity=1, current_capacity=0, 
                price=price, event_id=event_id
            )
            sections.append(section)
    else:
        section = Section(name=name, max_capacity=capacity, current_capacity=0, price=price, event_id=event_id)
        sections.append(section)
    return sections


def get_section_by_event(event_id):
    sections = Section.select().where(Section.event_id == event_id)
    response = {
        "event": event.to_dict(),
        "list_section": [section.to_dict() for section in sections]
    }
    return response


def get_section_detail(section_id):
    section = Section.get_or_none(Section.id == section_id)
    if section is None:
        raise ApplicationException("Section not exist")
    return section.to_dict()


def reduce_section_quantity(list_ticket_section):
    sections = []
    for ticket_section in list_ticket_section:
        section = Section.get_or_none(Section.id == ticket_section["id"])
        if section is None:
            raise ApplicationException("Section not exist")
        section.quantity -= int(ticket_section["quantity"])
        sections.append(section)
    for section in sections:
        section.save()
    return True


def add_section_quantity(list_ticket_section):
    sections = []
    for ticket_section in list_ticket_section:
        section = Section.get_or_none(Section.id == ticket_section["id"])
        if section is None:
            raise ApplicationException("Section not exist")
        section.quantity += int(ticket_section["quantity"])
        sections.append(section)
    for section in sections:
        section.save()
    return True


def validate_ticket_section(list_ticket_section):
    for ticket_section in list_ticket_section:
        section = Section.get_or_none(Section.id == ticket_section["id"])
        if section is None or section.quantity <= ticket_section["quantity"]:
            return False
    return True


def get_ticket_detail(ticket_id):
    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if ticket is None:
        raise ApplicationException("Ticket not exist")
    return ticket.to_dict()


def get_ticket_by_order(order_id):
    order = get_order(order_id)
    tickets = Ticket.select().where(Ticket.order_id == order_id)
    resp = [ticket.to_dict() for ticket in tickets]
    return resp


def generate_ticket(order_id, list_ticket_section):
    tickets, resp = [], []
    for ticket_section in list_ticket_section:
        id_section, quantity = ticket_section.get("id", 0), ticket_section.get("quantity", 0)
        if id_section <= 0 or quantity <= 0:
            raise ApplicationException("Wrong input")
        section = Section.get_or_none(Section.id == id_section)
        for i in range(quantity):
            ticket = Ticket(order_id=order_id, section=section)
            tickets.append(ticket)
    for ticket in tickets:
        ticket.save()
        resp.append(ticket.to_dict())
    return resp


def remove_ticket(order_id):
    tickets = Ticket.select().where(Ticket.order_id == order_id)
    for ticket in tickets:
        ticket.delete_instance()
    return True