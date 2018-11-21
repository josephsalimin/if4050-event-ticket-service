from .models import User
import bcrypt
from .exception import ApplicationException


def create_user(company_id, username, fullname, email, password, address):
    """
    Function to create user
    :param company_id: int
    :param username: string
    :param fullname: string
    :param email: string
    :param password: string
    :param address: string
    :return: dict
    """
    user = User.get_or_none(User.username == username, User.company_id == company_id)
    if user is not None:
        raise ApplicationException("User already exists")
    user = User.get_or_none(User.email == email, User.company_id == company_id)
    if user is not None:
        raise ApplicationException("User already exists")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(
        username=username,
        fullname=fullname,
        email=email,
        password=hashed_password,
        address=address,
        company_id=company_id
    )
    user.save()
    return user.to_dict()


def search_user(company_id, username="", email=""):
    """
    Function to search user based on username or email
    :param company_id: int
    :param username: string
    :param email: string
    :return: array of dict
    """
    users = User\
        .select()\
        .where(
            (User.username.contains(username) & User.company_id == company_id) |
            (User.email.contains(email) & User.company_id == company_id)
        )
    response = []
    for user in users:
        response.append(user.to_dict())
    return response


def get_user_detail(company_id, user_id):
    """
    Get user detail based on user id
    :param company_id: int
    :param user_id: int
    :return: dict
    """
    user = User.get_or_none(User.id == user_id, User.company_id == company_id)
    if user is None:
        raise ApplicationException("User not found!")
    return user.to_dict()


def update_user(company_id, user_id, fullname, address):
    """
    Update user based on user id
    :param company_id:
    :param user_id:
    :param fullname:
    :param address:
    :return:
    """
    user = User.get_or_none(User.id == user_id, User.company_id == company_id)
    if user is None:
        raise ApplicationException("User not found!", 400)
    user.update_attrs(fullname, address)
    user.save()
    return user.to_dict()
