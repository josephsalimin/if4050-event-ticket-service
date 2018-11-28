from spyne import ResourceNotFoundError, InternalError, ArgumentError
from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from .models import OrderPaymentRequest, OrderPaymentResp
from utils.payload_builder import build_payload
import requests


def create_request(user_id, order_id, instance_id, callback, callback_type, payment_method, auth_key, message_name):
    payload = {
        'auth_key': auth_key,
        'user_id': user_id,
        'order_id': order_id,
        'callback': callback,
        'callback_type': callback_type,
        'payment_method': payment_method
    }
    payload = build_payload(payload)
    payload['processInstanceId'] = instance_id
    payload['messageName'] = message_name
    return payload


class OrderPaymentService(ServiceBase):
    @rpc(OrderPaymentRequest, _returns=OrderPaymentResp)
    def OrderPayment(ctx, PaymentInput: OrderPaymentRequest):
        message_url = ctx.udc.message_url
        message_name = ctx.udc.message_name
        auth_key = ctx.udc.token
        # Get user_id, order_id, instance_id, and callback
        user_id = PaymentInput.user_id
        order_id = PaymentInput.order_id
        instance_id = PaymentInput.instance_id
        callback = PaymentInput.callback
        callback_type = PaymentInput.callback_type
        payment_method = PaymentInput.payment_method
        if (payment_method != 'ovo' and payment_method != 'go_pay' and payment_method != 'bank' and payment_method != 'bank_va'):
            raise ArgumentError("Payment method not available")
        # Create payload
        payload = create_request(user_id, order_id, instance_id, callback, callback_type, payment_method, auth_key, message_name)
        print(payload)
        camunda_resp = requests.post(message_url, json=payload)
        if camunda_resp.status_code == 404:
            raise ResourceNotFoundError(camunda_resp)
        elif not camunda_resp.ok:
            raise InternalError(Exception("Spyne Server Error"))
        return OrderPaymentResp(200, "Processing your input. Detail will be given to your callback URL")


