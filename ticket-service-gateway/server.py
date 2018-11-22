from wsgiref.simple_server import make_server
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from configparser import ConfigParser

from create_event.create_event_service import CreateEventService
from book_event.book_event_service import BookEventService
from cancel_order.cancel_order_service import CancelOrderService

config = ConfigParser()
config.read('config.ini')


class ConfigContext(object):
    def __init__(self):
        self.token = config["App"]["token"]
        self.create_event_url = config["CamundaService"]["create_event_url"]
        self.cancel_order_url = config["CamundaService"]["cancel_order_url"]
        self.book_event_url = config["CamundaService"]["book_event_url"]


def _on_method_call(ctx):
    ctx.udc = ConfigContext()


CreateEventService.event_manager.add_listener('method_call', _on_method_call)
application = Application([CreateEventService], 'spyne.examples.hello.http',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8000, wsgi_application)
    print("Serving in 127.0.0.1:8000")
    server.serve_forever()
