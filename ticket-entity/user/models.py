import time
import bcrypt
from peewee import *
from playhouse.shortcuts import model_to_dict
from .database import DatabaseManager


class BaseModel(Model):
    created_at = BigIntegerField(default=int(round(time.time() * 1000)))
    updated_at = BigIntegerField(default=int(round(time.time() * 1000)))

    class Meta:
        database = DatabaseManager.get_database()

    def save(self, force_insert=False, only=None):
        self.updated_at = int(round(time.time() * 1000))
        return super(BaseModel, self).save(force_insert, only)


class User(BaseModel):
    username = CharField(max_length=100, null=False, index=True)
    fullname = CharField(max_length=100, null=False, default="Anonymous")
    email = CharField(max_length=100, null=False, index=True)
    password = CharField(max_length=100, null=False)
    address = CharField(max_length=255, null=False)
    company_id = IntegerField(null=False, default=1)

    def validate_password(self, password):
        return bcrypt.checkpw(password, self.password)

    def update_attr(self, fullname, address):
        self.fullname = fullname
        self.address = address

    def to_dict(self):
        return model_to_dict(self, recurse=False, only=[User.id, User.username, User.fullname, User.email, User.address, User.company_id])

    class Meta:
        table_name = "users"
