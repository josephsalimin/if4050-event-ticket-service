from spyne import ResourceNotFoundError, InternalError
from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from .models import OrderPaymentRequest, OrderPaymentResp
from utils.payload_builder import build_payload
import requests


def create_request(user_id, order_id, instance_id, callback_url, auth_key, message_name):
    payload = {
        'auth_key': auth_key,
        'user_id': user_id,
        'order_id': order_id,
        'callback_url': callback_url
    }
    payload = build_payload(payload)
    payload['processInstanceId'] = instance_id
    payload['messageName'] = message_name
    return payload


class OrderPaymentService(ServiceBase):
    @rpc(OrderPaymentRequest, _returns=OrderPaymentResp)
    def OrderPayment(ctx, payment_request: OrderPaymentRequest):
        message_url = ctx.udc.message_url
        message_name = ctx.udc.message_name
        auth_key = ctx.udc.token
        # Get user_id, order_id, instance_id, and callback_url
        user_id = payment_request.user_id
        order_id = payment_request.order_id
        instance_id = payment_request.instance_id
        callback_url = payment_request.callback_url
        # Create payload
        payload = create_request(user_id, order_id, instance_id, callback_url, auth_key, message_name)
        print(payload)
        camunda_resp = requests.post(message_url, json=payload)
        if camunda_resp.status_code == 404:
            raise ResourceNotFoundError(camunda_resp)
        elif not camunda_resp.ok:
            raise InternalError(Exception("Spyne Server Error"))
        return OrderPaymentResp(200, "Processing your input. Detail will be given to your callback URL")


