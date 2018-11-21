from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from model import Event, Section, Orderline

import requests

def validateBookingRequest(ticket_url, orderline_list):
  validate_payload = {'section_list': []}
  for orderline in orderline_list:
    validate_payload['section_list'].append({'section_id' : orderline.section_id, 'quantity': orderline.quantity})
  validate_booking_resp = requests.post(ticket_url+'/event/validate', json=validate_payload)
  validate_booking_resp = get_event_resp.json()
  if(not validate_booking_resp.json()['success']):
    return False
  return True

def calculateOrder(ticket_url, orderline_list):
  total_price = 0
  for orderline in orderline_list:
    section_resp = requests.get(ticket_url+'/section/'+orderline.section_id, json=create_invoice_payload)
    section_json = section_resp.json()
    total_price += orderline.quantity * section_json["price"]

  return total_price
  
def createOrder(ticket_url, user_id, price):
  create_order_payload = {'user_id' : user_id, 'price': price}
  create_order_resp = requests.post(ticket_url+'/order', json=payload)
  return create_order_resp

def reserveTicket(ticket_url, order_id, orderline_list):
  reserve_ticket_payload = {'order_id': order_json["id"], 'section_list': orderline_list}
  reserve_ticket_resp = requests.post(ticket_url+'/invoice', json=create_invoice_payload)
  return reserve_ticket_resp    

class BookEventService(ServiceBase):
  @rpc(Integer, Iterable(Orderline), _returns=Iterable(Orderline))
  def BookEvent(ctx,user_id, orderline_list):
    ticket_url = ctx.udc.ticket_url
    payment_url = ctx.udc.payment_url
    if (validateBookingRequest(ticket_url, orderline_list)):
      total_price = calculateOrder(orderline_list)
      create_order_resp = createOrder(user_id, total_price)
      if (create_order_resp.ok):
        create_order_json = create_order_resp.json()
        order_id = create_order_json['order_id']
        reserve_ticket_resp = reserveTicket(order_id, orderline_list)
        if (reserve_ticket_resp.ok):
            return orderline_list

    return []
    

