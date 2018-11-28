from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.error import InternalError, ResourceNotFoundError
from .models import EventTicketRequest, EventTicketResp
from utils.payload_builder import build_payload
import requests


def create_request(event, list_section, callback, callback_type, auth_key):
    list_section_dict = [section.__dict__ for section in list_section]
    payload = {
        'auth_key': auth_key,
        'event': event.__dict__,
        'section_list': list_section_dict,
        'callback': callback,
        'callback_type': callback_type
    }
    return build_payload(payload)


class CreateEventService(ServiceBase):
    @rpc(EventTicketRequest, _returns=EventTicketResp)
    def CreateEvent(ctx, CreateEventInput: EventTicketRequest):
        create_event_url = ctx.udc.create_event_url
        # Get auth_key, event, list section, callback URL
        auth_key = ctx.udc.token
        event = CreateEventInput.event
        list_section = CreateEventInput.list_section
        callback_type = CreateEventInput.callback_type
        callback = CreateEventInput.callback
        # Create payload and request to create_event_url
        payload = create_request(event, list_section, callback, callback_type, auth_key)
        camunda_resp = requests.post(create_event_url, json=payload)
        if camunda_resp.status_code == 404:
            raise ResourceNotFoundError(camunda_resp)
        elif not camunda_resp.ok:
            raise InternalError(Exception("Spyne Server Error"))
        return EventTicketResp(200, "Processing your input. Detail will be given to your callback URL")
