from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Array


class Event(ComplexModel):
    __namespace__ = 'spyne.ticketx.service'
    __type_name__ = 'Event'

    name = Unicode
    location = Unicode
    partner_id = UnsignedInteger32
    start_at = Integer
    end_at = Integer
    description = Unicode


class Section(ComplexModel):
    __namespace__ = 'spyne.ticketx.service'
    __type_name__ = 'Section'

    name = Unicode
    capacity = Integer
    price = Integer
    has_seat = Boolean


class CreateEventRequest(ComplexModel):
    __namespace__ = 'spyne.ticketx.service'
    __type_name__ = 'CreateEventRequest'

    event = Event
    list_section = Array(Section)
    callback_url = Unicode


class CreateEventResponse(ComplexModel):
    __namespace__ = 'spyne.ticketx.service'
    __type_name__ = 'CreateEventResponse'

    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, status_code, message):
        super(CreateEventResponse, self).__init__()
        self.status_code = status_code
        self.message = message
