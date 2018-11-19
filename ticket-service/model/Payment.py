from spyne.model.primitive import Unicode, Integer, UnsignedInteger32
from spyne.model.complex import ComplexModel

class Payment(ComplexModel):
    __namespace__ = 'spyne.examples.user_manager'

    id = UnsignedInteger32
    order_id = UnsignedInteger32
    total_price = Integer