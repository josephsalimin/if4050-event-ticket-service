from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from model import Event, Section

import requests

def validateEventDetail(event, partner_url, auth_header):
  get_partner_resp = requests.get(partner_url+'/partner/', headers = auth_header)
  is_partner_valid = get_partner_resp.ok
  is_date_valid = event.start_at < event.end_at
  return is_partner_valid and is_date_valid

def addEvent(event_url, event, auth_header):
  create_event_payload = {
      'name': event.name, 
      'partner_id':event.partner_id, 
      'start_at': event.start_at, 
      'end_at': event.end_at, 
      'description': event.description, 
      'location': event.location}
  create_event_resp = requests.post(event_url+'/event', json = create_event_payload, headers=auth_header)
  return create_event_resp

def issueTicket(ticket_url, event_json, section_list, auth_header):
  event_id = event_json["id"]
  create_ticket_payload = {"event_id": event_id, "section_list": []}

  for section in section_list:
    create_ticket_payload["section_list"].append(
      {
        'name': section.name, 
        'capacity': section.capacity, 
        'price': section.price, 
        'has_seat': section.has_seat
      })

  print("Section list: " , create_ticket_payload)
  create_ticket_resp = requests.post(ticket_url+'/ticket_section', json = create_ticket_payload, headers=auth_header)
  return create_ticket_resp


class EventCreationService(ServiceBase):
  @rpc(Event, Iterable(Section), _returns=Boolean)
  def CreateEvent(ctx,event,section_list):
    ticket_url = ctx.udc.ticket_url;
    event_url = ctx.udc.event_url;
    partner_url = ctx.udc.partner_url;
    auth_header = {'Authorization': ctx.udc.token}

    if (not validateEventDetail(event, partner_url, auth_header)):
      return False
    create_event_resp = addEvent(event_url, event, auth_header)
    if (create_event_resp.ok):
      create_event_json = create_event_resp.json()
      create_ticket_resp = issueTicket(ticket_url, create_event_json, section_list, auth_header)
      if (create_ticket_resp.ok):
        return True
      else:
        return False
    else:
      return False

    


