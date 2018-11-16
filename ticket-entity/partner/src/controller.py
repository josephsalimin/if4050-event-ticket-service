from .models import Partner
from app_exception import ApplicationException


def create_partner(name, address, email, contact_number):
    partner = Partner.get_or_none(name=name)
    if partner is not None:
        raise ApplicationException("Partner exists")
    partner = Partner(
            name=name,
            address=address,
            email=email,
            contact_number=contact_number
        )
    partner.save()
    return partner.to_dict()


def get_list_partner(name):
    partners = Partner.select().where(Partner.name.contains(name.lower()))
    response = []
    for partner in partners:
        response.append(partner.to_dict())
    return response


def get_partner_detail(partner_id):
    partner = Partner.get_or_none(Partner.id == partner_id)
    if partner is None:
        raise ApplicationException("Partner not exist")
    return partner.to_dict()


def update_partner(partner_id, name, address, email, contact_number):
    partner = Partner.get_or_none(Partner.id == partner_id)
    if partner is None:
        raise ApplicationException("Partner not exist")
    partner.update_attr(name, address, email, contact_number)
    partner.save()
    return partner.to_dict()