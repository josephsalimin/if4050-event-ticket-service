from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Iterable


class Event(ComplexModel):
    __namespace__ = 'create_event_service'

    name = Unicode
    location = Unicode
    partner_id = UnsignedInteger32
    start_at = Integer
    end_at = Integer
    description = Unicode


class Section(ComplexModel):
    __namespace__ = 'create_event_service'

    id = UnsignedInteger32
    name = Unicode
    event_id = UnsignedInteger32
    capacity = Integer
    price = Integer
    has_seat = Boolean


class CreateEventRequest(ComplexModel):
    __namespace__ = 'create_event_service'

    event = Event
    list_section = Iterable(Section)
    callback_url = Unicode


class CreateEventResponse(ComplexModel):
    __namespace__ = 'create_event_service'

    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, status_code, message):
        super(CreateEventResponse, self).__init__()
        self.status_code = status_code
        self.message = message
