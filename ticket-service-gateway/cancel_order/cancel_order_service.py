from spyne import ResourceNotFoundError, InternalError
from spyne.decorator import rpc
from spyne.service import ServiceBase
from .models import CancelOrderRequest, CancelOrderResponse
from utils.payload_builder import build_payload
import requests


def create_request(order_id, callback_url, auth_key):
    payload = {
        'auth_key': auth_key,
        'order_id': order_id,
        'callback_url': callback_url
    }
    return build_payload(payload)


class CancelOrderService(ServiceBase):
    @rpc(CancelOrderRequest, _returns=CancelOrderResponse)
    def CancelOrder(ctx, CancelOrderInput: CancelOrderRequest):
        cancel_order_url = ctx.udc.cancel_order_url
        auth_key = ctx.udc.token
        order_id = CancelOrderInput.order_id
        callback_url = CancelOrderInput.callback_url
        # Create payload and request to create_event_url
        payload = create_request(order_id, callback_url, auth_key)
        camunda_resp = requests.post(cancel_order_url, json=payload)
        print(camunda_resp.json())
        if camunda_resp.status_code == 404:
            raise ResourceNotFoundError(camunda_resp)
        elif not camunda_resp.ok:
            raise InternalError(Exception("Spyne Server Error"))
        return CancelOrderResponse(200, "Processing your input. Detail will be given to your callback URL")
