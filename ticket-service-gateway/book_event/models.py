from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Iterable


class Section(ComplexModel):
    __namespace__ = 'spyne.ticketx.service'

    id = UnsignedInteger32
    quantity = UnsignedInteger32
    price = Integer


class BookEventRequest(ComplexModel):
    __namespace__ = 'spyne.ticketx.service'

    user_id = Integer
    section_list = Iterable(Section)
    callback_url = Unicode


class BookEventResponse(ComplexModel):
    __namespace__ = 'spyne.ticketx.service'

    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, instance_id, status_code, message):
        super(CancelOrderResponse, self).__init__()
        self.instance_id = instance_id
        self.status_code = status_code
        self.message = message