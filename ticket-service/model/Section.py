from spyne.model.primitive import Unicode, Boolean, Integer, UnsignedInteger32
from spyne.model.complex import ComplexModel

class Section(ComplexModel):
    __namespace__ = 'spyne.examples.user_manager'

    id = UnsignedInteger32
    name = Unicode
    event_id = UnsignedInteger32
    capacity = Integer
    price = Integer
    has_seat = Boolean