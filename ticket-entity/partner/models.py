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


class Partner(BaseModel):
    name = CharField(max_length=100, null=False, unique=True, index=True)
    address = CharField(max_length=255, null=False)
    email = CharField(max_length=100, null=False, unique=True, index=True)
    contact_number = CharField(max_length=20, null=False)

    def update_attr(self, name, address, email, contact_number):
        self.name = name
        self.address = address
        self.email = email
        self.contact_number = contact_number

    def to_dict(self):
        return model_to_dict(self, recurse=False)

    class Meta:
        table_name = "partners"