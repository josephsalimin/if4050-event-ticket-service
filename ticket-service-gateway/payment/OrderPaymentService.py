from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from model import Event, Section, Payment


import requests

def validatePayment(payment, order_url, auth_header):
  get_order_resp = requests.get(order_url+'/order/'+payment.order_id)
  return get_order_resp.ok

def sendPayment(payment, payment_url):
  payload = {'payment': payment}
  send_payment_resp = requests.post(order_url+'/order/'+payment.order_id, json=payload)
  return send_payment_resp.ok

def setOrderStatusToPaid(order_id, order_url, auth_header):
  payload = {'status' : 'paid'}
  update_order_resp = requests.put(order_url+'/order/'+order_id, json=payload, headers = auth_header)
  return update_order_resp.ok

class OrderPaymentService(ServiceBase):
  @rpc(Payment, _returns=Boolean)
  def OrderPayment(ctx,payment):
    order_url  = ctx.udc.order_url
    payment_url  = ctx.udc.payment_url
    auth_header = {'Authorization': ctx.udc.token}
    
    if (validatePayment(payment, order_url, auth_header)):
      if (sendPayment(payment, payment_url)):
        return setOrderStatusToPaid(payment.order_id, order_url, auth_header)

    return False



    


