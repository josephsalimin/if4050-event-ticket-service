from spyne import ResourceNotFoundError, InternalError
from spyne.decorator import rpc 
from spyne.model.complex import Iterable
from spyne.model.primitive import Unicode, Boolean, Integer
from spyne.service import ServiceBase
from datetime import datetime
from .models import OrderPaymentRequest, OrderPaymentResponse
from utils.payload_builder import build_payload
import requests


def create_request(user_id, order_id, instance_id, callback_url, tenant_id, auth_key, message_name):
    list_section_dict = [section.__dict__ for section in list_section]
    payload = {
        'auth_key': auth_key,
        'user_id': user_id,
        'section_list': list_section_dict,
        'callback_url': callback_url
    }
    return build_payload(payload)


class OrderPaymentService(ServiceBase):
    @rpc(OrderPaymentRequest, _returns=OrderPaymentResponse)
    def OrderPayment(ctx, payment_request: OrderPaymentRequest):
        message_url = ctx.udc.message_url
        message_name = ctx.udc.message_name
        tenant_id = ctx.udc.book_env_tenant_id
        auth_key = ctx.udc.token
        # Get user_id, order_id, instance_id, and callback_url
        user_id = OrderPaymentRequest.user_id
        order_id = OrderPaymentRequest.order_id
        instance_id = OrderPaymentRequest.instance_id
        callback_url = OrderPaymentRequest.callback_url
        # Create payload
        payload = create_request(user_id, order_id, instance_id, callback_url, tenant_id, auth_key, message_name)
        payload = build_payload(payload)
        camunda_resp = requests.post(message_url, json=payload)
        if camunda_resp.status_code == 404:
            raise ResourceNotFoundError(camunda_resp)
        elif not camunda_resp.ok:
            raise InternalError(Exception("Spyne Server Error"))
        return BookEventResponse(200, "Processing your input. Detail will be given to your callback URL")


