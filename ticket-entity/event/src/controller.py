from app_exception import ApplicationException
from .models import Event
import time


# TODO: create_event return jwt too :/

def create_event(partner_id, name, description, location, start_at, end_at):
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
    event = Event.get_or_none(Event.id == event_id, Event.partner_id == partner_id)
    if event is None:
        raise ApplicationException("Event not exist")
    event.update_attr(name, description, location, start_at, end_at)
    event.save()
    return event.to_dict()


def get_event_detail(event_id):
    event = Event.get_or_none(Event.id == event_id)
    if event is None:
        raise ApplicationException("Event not exist")
    return event.to_dict()


def get_list_event_history():
    time_now = round(time.time())
    events = Event.select().where(Event.end_at < time_now)
    response = [event.to_dict() for event in events]
    return response


def get_list_event_available():
    time_now = round(time.time())
    events = Event.select().where(Event.start_at >= time_now)
    response = [event.to_dict() for event in events]
    return response


def get_events_by_partner(partner_id):
    events = Event.select().where(Event.partner_id == partner_id)
    response = []
    response = [event.to_dict() for event in events]
    return response
