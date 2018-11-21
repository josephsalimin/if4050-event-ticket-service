from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Iterable

class CancelOrderRequest(ComplexModel):
    __namespace__ = 'cancel_order_service'

    order_id = Integer


class CancelOrderResponse(ComplexModel):
    __namespace__ = 'cancel_order_service'

    status_code = UnsignedInteger32
    message = Unicode

    def __init__(self, status_code, message):
        super(CancelOrderResponse, self).__init__()
        self.status_code = status_code
        self.message = message
