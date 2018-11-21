from .models import Partner
from .exception import ApplicationException


def create_partner(name, address, email, contact_number):
    """
    Function to create partner
    :param name: string
    :param address: string
    :param email: string
    :param contact_number: string, must number
    :return: dict
    """
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
    """
    Get list partner by name
    :param name: string
    :return: array of dict
    """
    partners = Partner.select().where(Partner.name.contains(name.lower()))
    response = [partner.to_dict() for partner in partners]
    return response


def get_partner_detail(partner_id):
    """
    Get partner detail from partner id
    :param partner_id:
    :return:
    """
    partner = Partner.get_or_none(Partner.id == partner_id)
    if partner is None:
        raise ApplicationException("Partner not exist")
    return partner.to_dict()


def update_partner(partner_id, name, address, email, contact_number):
    """
    Update partner based on partner id
    :param partner_id: int
    :param name: string
    :param address: string
    :param email: string
    :param contact_number: string
    :return: dict
    """
    partner = Partner.get_or_none(Partner.id == partner_id)
    if partner is None:
        raise ApplicationException("Partner not exist")
    partner.update_attr(name, address, email, contact_number)
    partner.save()
    return partner.to_dict()
