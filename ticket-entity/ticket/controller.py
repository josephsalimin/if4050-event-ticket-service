from .exception import ApplicationException
from .models import Ticket, Section


def issue_ticket(event_id, list_ticket_section):
    """
    Function to issue ticket section
    :param event_id: int
    :param list_ticket_section: array of dict
    :return: boolean
    """
    sections = []
    for ticket_section in list_ticket_section:
        try:
            name, price = ticket_section["name"], ticket_section["price"]
            capacity, has_seat = ticket_section["capacity"], ticket_section["has_seat"]
        except KeyError:
            raise ApplicationException("Wrong input", 400)
        sections += create_ticket_section(has_seat, event_id, name, price, capacity)
    for section in sections:
        section.save()
    return True


def create_ticket_section(has_seat, event_id, name, price, capacity):
    """
    Function to create ticket section
    :param has_seat: boolean
    :param event_id: int
    :param name: string
    :param price: int
    :param capacity: int
    :return: array of Section
    """
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
    """
    Function to get Section from event
    :param event_id: int
    :return: array of dict
    """
    sections = Section.select().where(Section.event_id == event_id)
    return [section.to_dict() for section in sections]


def get_section_detail(section_id):
    """
    Function to get section detail
    :param section_id: int
    :return: dict
    """
    section = Section.get_or_none(Section.id == section_id)
    if section is None:
        raise ApplicationException("Section not exist")
    return section.to_dict()


def change_section_capacity(list_ticket_section, change_type):
    """
    Function to change section capacity
    :param list_ticket_section: array of dict
    :param change_type: string
    :return: boolean
    """
    sections = []
    for ticket_section in list_ticket_section:
        section = Section.get_or_none(Section.id == ticket_section["id"])
        if section is None:
            return False
        if change_type == 'reduce':
            section.current_capacity -= int(ticket_section["quantity"])
        elif change_type == 'add':
            section.current_capacity += int(ticket_section["quantity"])
        sections.append(section)
    for section in sections:
        section.save()
    return True


def validate_ticket_section(list_ticket_section):
    """
    Function to validate ticket section
    :param list_ticket_section: array of dict
    :return: boolean
    """
    for ticket_section in list_ticket_section:
        section = Section.get_or_none(Section.id == ticket_section["id"])
        if section is None or section.max_capacity - section.current_capacity < ticket_section["quantity"]:
            return False
    return True


def get_ticket_detail(ticket_id):
    """
    Function to get ticket detail
    :param ticket_id: int
    :return: dict
    """
    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if ticket is None:
        raise ApplicationException("Ticket not exist")
    return ticket.to_dict()


def get_ticket_by_order(order_id):
    """
    Function to get ticket from order_id
    :param order_id: int
    :return: array of dict
    """
    tickets = Ticket.select().where(Ticket.order_id == order_id)
    resp = [ticket.to_dict() for ticket in tickets]
    return resp


def generate_ticket(order_id, list_ticket_section):
    """
    Function to generate ticket after pay book
    :param order_id: int
    :param list_ticket_section: array of dict
    :return: array of dict
    """
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
    """
    Function to delete ticket from order
    :param order_id: id
    :return: boolean
    """
    tickets = Ticket.select().where(Ticket.order_id == order_id)
    for ticket in tickets:
        ticket.delete_instance()
    return True
