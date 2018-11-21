from spyne.model.primitive import Unicode, Integer, UnsignedInteger32, Boolean
from spyne.model.complex import ComplexModel, Iterable


class Section(ComplexModel):
    __namespace__ = 'create_event_service'

    id = UnsignedInteger32
    name = Unicode
    event_id = UnsignedInteger32
    capacity = Integer
    price = Integer
    has_seat = Boolean


class Order(ComplexModel):
  __namespace__ = 'book_event_service'

  user_id = Integer
  total_price = Integer
  section_list = Iterable(Section)


class BookEventRequest(ComplexModel):
  __namespace__ = 'book_event_service'

  order = Order


class BookEventResponse(ComplexModel):
  __namespace__ = 'book_event_service'

  status_code = UnsignedInteger32
  message = Unicode

  def __init__(self, status_code, message):
      super(CancelOrderResponse, self).__init__()
      self.status_code = status_code
      self.message = message
