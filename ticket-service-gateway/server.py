from wsgiref.simple_server import make_server
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter
from configparser import ConfigParser

from create_event.create_event_service import CreateEventService
from book_event.book_event_service import BookEventService
from payment.order_payment_service import OrderPaymentService
from cancel_order.cancel_order_service import CancelOrderService


config = ConfigParser()
config.read('config.ini')


class ConfigContext(object):
    def __init__(self):
        self.token = config["App"]["token"]
        self.create_event_url = config["CamundaService"]["create_event_url"]
        self.cancel_order_url = config["CamundaService"]["cancel_order_url"]
        self.book_event_url = config["CamundaService"]["book_event_url"]
        self.message_url = config["CamundaService"]["message_url"]
        self.message_name = config["CamundaService"]["message_name"]



def _on_method_call(ctx):
    ctx.udc = ConfigContext()


CreateEventService.event_manager.add_listener('method_call', _on_method_call)
BookEventService.event_manager.add_listener('method_call', _on_method_call)
OrderPaymentService.event_manager.add_listener('method_call', _on_method_call)
CancelOrderService.event_manager.add_listener('method_call', _on_method_call)
application_1 = Application([CreateEventService], 'spyne.ticketx.event',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
application_2 = Application([CancelOrderService], 'spyne.ticketx.cancel',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
application_3 = Application([BookEventService, OrderPaymentService], 'spyne.ticketx.book',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())           

wsgi_application = WsgiMounter({
    'create_event': application_1,
    'cancel_order': application_2,
    'book_event': application_3
})

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8000, wsgi_application)
    print("Serving in 127.0.0.1:8000")
    server.serve_forever()
