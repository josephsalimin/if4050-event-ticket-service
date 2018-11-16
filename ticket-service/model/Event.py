from spyne.model.primitive import Unicode, Integer, UnsignedInteger32
from spyne.model.complex import ComplexModel

class Event(ComplexModel):
    __namespace__ = 'spyne.examples.user_manager'

    id = UnsignedInteger32
    name = Unicode
    location = Unicode
    partner_id = UnsignedInteger32
    start_at = Integer
    end_at = Integer
    description = Unicode