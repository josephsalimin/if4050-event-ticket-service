from spyne.decorator import rpc
from spyne.service import ServiceBase
from .models import CreateEventRequest, CreateEventResponse, Section, Event
import requests


def create_request(event, list_section):
    payload = {}
    return payload


class CreateEventService(ServiceBase):
    @rpc(CreateEventRequest, _returns=CreateEventResponse)
    def create_event(ctx, event_request: CreateEventRequest):
        auth_header = {'Authorization': ctx.udc.token}
        # Get event and list section
        event = event_request.event
        list_section = event_request.list_section
        # Stubs
        # TODO: request POST to Camunda
        return CreateEventResponse(200, "Correct")
