from wsgiref.simple_server import make_server

from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from configparser import ConfigParser

from service import EventCreationService, BookEventService, CancelBookingService

config = ConfigParser()
config.read('config.ini')

class ConfigContext(object):
    def __init__(self):
        self.ticket_url = config["TicketService"]["base_url"]
        self.payment_url = config["PaymentService"]["base_url"]


def _on_method_call(ctx):
  ctx.udc = ConfigContext()

EventCreationService.event_manager.add_listener('method_call', _on_method_call)
application = Application([EventCreationService], 'ticketx.test.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
  print(config["Database"]["host"])
  server = make_server('127.0.0.1', 8000, wsgi_application)
  server.serve_forever()
