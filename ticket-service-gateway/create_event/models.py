from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Array


class Event(ComplexModel):
    __namespace__ = 'spyne.ticketx.event'

    name = Unicode
    location = Unicode
    partner_id = UnsignedInteger32
    start_at = Integer
    end_at = Integer
    description = Unicode


class EventSection(ComplexModel):
    __namespace__ = 'spyne.ticketx.event'

    name = Unicode
    capacity = Integer
    price = Integer
    has_seat = Boolean


class EventTicketRequest(ComplexModel):
    __namespace__ = 'spyne.ticketx.event'

    event = Event
    list_section = Array(EventSection)
    callback = Unicode
    callback_type = Unicode


class EventTicketResp(ComplexModel):
    __namespace__ = 'spyne.ticketx.event'

    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, status_code, message):
        super(EventTicketResp, self).__init__()
        self.status_code = status_code
        self.message = message
