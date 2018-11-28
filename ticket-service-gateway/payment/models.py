from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Iterable


class OrderPaymentRequest(ComplexModel):
    __namespace__ = 'spyne.ticketx.book'

    user_id = Integer
    order_id = Integer
    instance_id = Unicode
    payment_method = Unicode
    callback = Unicode
    callback_type = Unicode


class OrderPaymentResp(ComplexModel):
    __namespace__ = 'spyne.ticketx.book'

    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, status_code, message):
        super(OrderPaymentResp, self).__init__()
        self.status_code = status_code
        self.message = message
