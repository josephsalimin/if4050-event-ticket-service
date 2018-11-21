from spyne.decorator import rpc
from spyne.service import ServiceBase
from .models import CreateEventRequest, CreateEventResponse, Section, Event
from util.payload_builder import build_payload
import requests


def create_request(event, list_section):
    payload = {}
    return payload


class CreateEventService(ServiceBase):
    @rpc(CreateEventRequest, _returns=CreateEventResponse)
    def create_event(ctx, event_request: CreateEventRequest):
        create_event_url = ctx.udc.create_event_url

        auth_header = {'Authorization': ctx.udc.token}
        # Get event and list section
        event = event_request.event
        list_section = event_request.list_section
        
        args_dict = {
            'auth_key': auth_header,
            'event': event.__dict__, 
            'section_list': list_section.__dict__, 
            'callback_url':event_request.callback_url}
                    
        payload = build_payload(args_dict)
        camunda_resp = requests.post(create_event_url, json=payload)
        
        if not camunda_resp.ok:
            CreateEventResponse(400, "Bad Request")
        return CreateEventResponse(200, "Correct")
