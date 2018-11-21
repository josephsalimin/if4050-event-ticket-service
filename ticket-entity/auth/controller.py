from .exception import ApplicationException
from .models import AuthService
import os
import jwt
import time


def create_auth_service(name, auth_type, partner_id=0):
    """
    Function to create Auth Service before using other REST Service
    :param name: string
    :param auth_type: string
    :param partner_id: int or string
    :return: dict
    """
    auth_service = AuthService.get_or_none(AuthService.name == name)
    if auth_service is not None:
        raise ApplicationException("Auth user already exist")
    auth_service = AuthService(name=name, auth_type=auth_type, partner_id=partner_id)
    auth_service.save()
    # Payload for JWT Token
    payload = {
        'id': auth_service.id,
        'partner_id': partner_id,
        'name': name,
        'auth_type': auth_type,
        'timestamp': time.time() * 1000
    }
    # Create auth and refresh token then save to database
    refresh_token = jwt.encode(payload, os.environ.get("REFRESH_KEY"), algorithm='HS256')\
        .decode('utf-8')
    auth_token = jwt.encode(payload, os.environ.get("AUTH_KEY"), algorithm='HS256')\
        .decode('utf-8')
    # Save auth service
    auth_service.refresh_token = refresh_token
    auth_service.auth_token = auth_token
    auth_service.save()
    return auth_service.to_dict()


def refresh_auth_token(name, refresh_token):
    """
    Function to refresh authentication token
    :param name: string
    :param refresh_token: string
    :return: dict
    """
    try:
        decode = jwt.decode(refresh_token, os.environ.get("REFRESH_KEY"), algorithms='HS256')
    except jwt.InvalidTokenError:
        raise ApplicationException("Not authenticated")
    auth_id = decode.get("id", 0)
    auth_service = AuthService.get_or_none(AuthService.id == auth_id)
    if auth_service is None:
        raise ApplicationException("Not exist")
    if auth_service.name != name:
        raise ApplicationException("Not authenticated")
    # Payload for JWT Token
    payload = {
        'id': auth_service.id,
        'partner_id': auth_service.partner_id,
        'name': name,
        'auth_type': auth_service.auth_type,
        'timestamp': time.time() * 1000
    }
    # Decode the auth token
    auth_token = jwt.encode(payload, os.environ.get("AUTH_KEY"), algorithm='HS256')
    auth_service.auth_token = auth_token.decode('utf-8')
    auth_service.save()
    return auth_service.to_dict()


def verify_auth(auth_token):
    """
    Function to verify authentication token
    :param auth_token: string
    :return: dict
    """
    try:
        decode = jwt.decode(auth_token, os.environ.get("AUTH_KEY"), algorithms='HS256')
    except jwt.InvalidTokenError:
        return {'valid': False}
    auth_service = AuthService.get_or_none(AuthService.id == decode.get("id", 0))
    if auth_service is None:
        return {'valid': False}
    auth_type = decode.get("auth_type", None)
    resp = {
        'id': decode.get("id", 0),
        'auth_type': auth_type,
        'partner_id': auth_service.partner_id,
        'valid': True
    }
    return resp


def get_auth(auth_id):
    """
    Function to get auth info
    :param auth_id:
    :return: dict
    """
    auth_service = AuthService.get_or_none(AuthService.id == auth_id)
    if auth_service is None:
        raise ApplicationException("Auth not exist")
    return auth_service.to_dict()