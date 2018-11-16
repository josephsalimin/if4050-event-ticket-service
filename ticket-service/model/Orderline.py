from spyne.model.primitive import Unicode, Integer, UnsignedInteger32
from spyne.model.complex import ComplexModel

class Orderline(ComplexModel):
    __namespace__ = 'spyne.examples.user_manager'

    id = UnsignedInteger32
    section_id = UnsignedInteger32
    quantity = Integer