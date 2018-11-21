from spyne.decorator import rpc 
from spyne.model.complex import Array
from spyne.model.primitive import Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from models import CancelOrderRequest, CancelOrderResponse
import requests

class CancelOrderService(ServiceBase):
  @rpc(CancelOrderRequest, _returns=CancelOrderResponse)
  def CancelOrder(ctx, order_request:CancelOrderRequest):
    cancel_order_url = ctx.udc.cancel_order_url
    auth_header = {'Authorization': ctx.udc.token}
    # Get event and list section
    order_id = order_request.order_id

    args_dict = {
      'auth_key': auth_header,
      'order_id': order_id, 
      'callback_url':event_request.callback_url 
      }
      
    payload = build_payload(args_dict)
    camunda_resp = requests.post(cancel_order_url, json=payload)
    
    if (not camunda_resp.ok):
      return CancelOrderResponse(400, "Bad Request")
      
    return CancelOrderResponse(200, "Correct")

    