from .exception import ApplicationException
from .models import Event
import time


def create_event(partner_id, name, description, location, start_at, end_at):
    """
    Function to create new Event, only Partner can create event
    :param partner_id: int
    :param name: string
    :param description: string
    :param location: string
    :param start_at: int
    :param end_at: int
    :return: dict
    """
    event = Event.get_or_none(Event.name == name, Event.partner_id == partner_id)
    if event is not None:
        raise ApplicationException("Event already exists")
    event = Event(
        name=name,
        description=description,
        location=location,
        start_at=start_at,
        end_at=end_at,
        partner_id=partner_id
    )
    event.save()
    return event.to_dict()


def update_event(event_id, partner_id, name, description, location, start_at, end_at):
    """
    Function to update event, only partner can do it
    :param event_id: int
    :param partner_id: int
    :param name: string
    :param description: string
    :param location: string
    :param start_at: int
    :param end_at: int
    :return: dict
    """
    event = Event.get_or_none(Event.id == event_id, Event.partner_id == partner_id)
    if event is None:
        raise ApplicationException("Event not exist")
    event.update_attr(name, description, location, start_at, end_at)
    event.save()
    return event.to_dict()


def delete_event(event_id, partner_id):
    """
    Function to delete event
    :param event_id: int
    :param partner_id: int
    :return: bool
    """
    event = Event.get_or_none(Event.id == event_id, Event.partner_id == partner_id)
    if event is not None:
        event.delete_instance()
    return True


def get_event_detail(event_id):
    """
    Function to get event detail by event_id
    :param event_id: int
    :return: dict
    """
    event = Event.get_or_none(Event.id == event_id)
    if event is None:
        raise ApplicationException("Event not exist")
    return event.to_dict()


def get_list_event_history():
    """
    Function to get list event history
    :return: array of dict
    """
    time_now = round(time.time())
    events = Event.select().where(Event.end_at < time_now)
    response = [event.to_dict() for event in events]
    return response


def get_list_event_available():
    """
    Function to get list event available
    :return: array of dict
    """
    time_now = round(time.time())
    events = Event.select().where(Event.start_at >= time_now)
    response = [event.to_dict() for event in events]
    return response


def get_events_by_partner(partner_id):
    """
    Function to get list event by partner_id
    :param partner_id: int
    :return: array of dict
    """
    events = Event.select().where(Event.partner_id == partner_id)
    response = [event.to_dict() for event in events]
    return response
