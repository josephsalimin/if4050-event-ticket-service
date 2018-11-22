from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.error import InternalError, ResourceNotFoundError
from .models import CreateEventRequest, CreateEventResponse
from utils.payload_builder import build_payload
import requests


def create_request(event, list_section, callback_url, auth_key):
    list_section_dict = [section.__dict__ for section in list_section]
    payload = {
        'auth_key': auth_key,
        'event': event.__dict__,
        'section_list': list_section_dict,
        'callback_url': callback_url
    }
    return build_payload(payload)


class CreateEventService(ServiceBase):
    @rpc(CreateEventRequest, _returns=CreateEventResponse)
    def CreateEvent(ctx, CreateEventInput: CreateEventRequest):
        create_event_url = ctx.udc.create_event_url
        # Get auth_key, event, list section, callback URL
        auth_key = ctx.udc.token
        event = CreateEventInput.event
        list_section = CreateEventInput.list_section
        callback_url = CreateEventInput.callback_url
        # Create payload and request to create_event_url
        payload = create_request(event, list_section, callback_url, auth_key)
        camunda_resp = requests.post(create_event_url, json=payload)
        print(payload["variables"])
        print(camunda_resp.json())
        if camunda_resp.status_code == 404:
            raise ResourceNotFoundError(camunda_resp)
        elif not camunda_resp.ok:
            raise InternalError(Exception("Spyne Server Error"))
        return CreateEventResponse(200, "Processing your input. Detail will be given to your callback URL")
