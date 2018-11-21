from spyne.decorator import rpc 
from spyne.model.complex import Array
from spyne.model.primitive import Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
import requests

def get_order_status(ticket_url,order_id):
  order_resp = requests.get(ticket_url+'/order/'+order_id, data = payload)
  if (order_resp.ok):
    order = order_resp.json()
    return order['status']
  else:
    return False


def refund_payment(payment_url, invoice_id):
  refund_payload = {'invoice_id': invoice_id}
  refund_resp = requests.post(payment_url+'/refund', json=refund_payload)
  return refund_resp

def cancel_order(ticket_url, order_id):
  cancel_order_resp = requests.delete(ticket_url+'/order/'+order_id)
  return cancel_order_resp

def release_ticket(ticket_url, section_list):
  release_ticket_payload = {'section_list' : section_list}
  release_ticket_resp = requests.post(ticket_url+'/ticket/release', json=release_ticket_payload)
  return release_ticket_resp

def remove_ticket(ticket_url, order_id):
  remove_ticket_resp = requests.delete(ticket_url+'/ticket/'+order_id)
  return remove_ticket_resp

class CancelBookingService(ServiceBase):
  @rpc(Integer, Integer, _returns=Boolean)
  def CancelTicket(ctx,order_id, invoice_id):
    ticket_url = ctx.ticket_url;
    payment_url = ctx.payment_url;
    order_status = get_order_status(order_id)
    if (order_status != 'cancel' and order_status != False):      
      cancel_order_resp = cancel_order(ticket_url, order_id)
      if (cancel_order_resp.ok):
        section_list = cancel_order_resp.json()

      if (order_status == 'paid'):
        refund_resp = refund_payment(invoice_id)
        if (not refund_resp.ok):
          return False
        
        remove_ticket_resp = remove_ticket(ticket_url, order_id)
        if (not remove_ticket_resp.ok):
          return False
      return True
    return False


