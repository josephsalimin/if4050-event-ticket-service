from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Iterable


class CancelOrderRequest(ComplexModel):
    __namespace__ = 'spyne.ticketx.cancel'

    order_id = Integer
    callback = Unicode
    callback_type = Unicode
    payment_method = Unicode


class CancelOrderResp(ComplexModel):
    __namespace__ = 'spyne.ticketx.cancel'

    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, status_code, message):
        super(CancelOrderResp, self).__init__()
        self.status_code = status_code
        self.message = message
