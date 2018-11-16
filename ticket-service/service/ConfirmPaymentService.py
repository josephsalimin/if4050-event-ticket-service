from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from model import Event, Section

import requests

class ConfirmPaymentService(ServiceBase):
  @rpc(Integer, _returns=Boolean)
  def ConfirmPayment(ctx,order_id):
    ticket_url = ctx.ticket_url
    payload = {'status': "paid"}
    update_event_resp = requests.put(ticket_url+'/event/'+order_id, json=payload)
    if (update_event_resp.ok):
      return True
    else :
      return False



    


