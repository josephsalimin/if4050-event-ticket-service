from .models import User
import bcrypt
from app_exception import ApplicationException


def create_user(company_id, username, fullname, email, password, address):
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
    user = User.get_or_none(User.id == user_id, User.company_id == company_id)
    if user is None:
        raise ApplicationException("User not found!")
    return user.to_dict()


def update_user(company_id, user_id, fullname, address):
    user = User.get_or_none(User.id == user_id, User.company_id == company_id)
    if user is None:
        raise ApplicationException("User not found!", 400)
    user.update_attrs(fullname, address)
    user.save()
    return user.to_dict()
