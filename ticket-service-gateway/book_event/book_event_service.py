from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from .models import BookEventRequest, BookEventResponse

import requests

class BookEventService(ServiceBase):
  @rpc(BookEventRequest, _returns=BookEventResponse)
  def BookEvent(ctx,book_event_request:BookEventRequest):
    book_event_url = ctx.udc.book_event_url
    auth_header = {'Authorization': ctx.udc.token}
    # Get event and list section

    args_dict = {
      'auth_key': auth_header,
      'order': book_event_request.order.__dict__, 
      'callback_url':event_request.callback_url 
      }
      
    payload = build_payload(args_dict)
    camunda_resp = requests.post(book_event_url, json=payload)
    
    if (not camunda_resp.ok):
      return BookEventResponse(400, "Bad Request")
    return BookEventResponse(200, "Correct")


