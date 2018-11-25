from spyne import ResourceNotFoundError, InternalError
from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from .models import BookEventRequest, BookEventResponse
from utils.payload_builder import build_payload
import requests


def create_request(user_id, list_section, callback_url, auth_key):
    list_section_dict = [section.__dict__ for section in list_section]
    payload = {
        'auth_key': auth_key,
        'user_id': user_id,
        'section_list': list_section_dict,
        'callback_url': callback_url
    }
    return build_payload(payload)


class BookEventService(ServiceBase):
    @rpc(BookEventRequest, _returns=BookEventResponse)
    def BookEvent(ctx, book_event_request: BookEventRequest):
        book_event_url = ctx.udc.book_event_url
        auth_key = ctx.udc.token
        # Get section_list, user_id, and callback_url
        section_list = BookEventRequest.section_list
        user_id = BookEventRequest.user_id
        callback_url = BookEventRequest.callback_url
        # Create payload and post to request
        payload = create_request(user_id, section_list, callback_url, auth_key)
        payload = build_payload(payload)
        camunda_resp = requests.post(book_event_url, json=payload)
        if camunda_resp.status_code == 404:
            raise ResourceNotFoundError(camunda_resp)
        elif not camunda_resp.ok:
            raise InternalError(Exception("Spyne Server Error"))
        json_response = camunda_resp.json()
        return BookEventResponse(json_response["id"], 200, "Processing your input. Detail will be given to your callback URL")
