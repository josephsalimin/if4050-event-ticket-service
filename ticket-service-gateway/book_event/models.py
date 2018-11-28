from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Iterable


class BookEventSection(ComplexModel):
    __namespace__ = 'spyne.ticketx.book'

    id = UnsignedInteger32
    quantity = UnsignedInteger32
    price = Integer


class BookEventRequest(ComplexModel):
    __namespace__ = 'spyne.ticketx.book'

    user_id = Integer
    section_list = Iterable(BookEventSection)
    callback = Unicode
    callback_type = Unicode


class BookEventResp(ComplexModel):
    __namespace__ = 'spyne.ticketx.book'

    instance_id = Unicode
    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, instance_id, status_code, message):
        super(BookEventResp, self).__init__()
        self.instance_id = instance_id
        self.status_code = status_code
        self.message = message
