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


class Section(BaseModel):
    name = CharField(max_length=100, null=False)
    max_capacity = IntegerField(null=False)
    current_capacity = IntegerField(null=False)
    price = IntegerField(null=False)
    event_id = IntegerField(null=False)

    def to_dict(self):
        return model_to_dict(self, recurse=False)

    class Meta:
        table_name = "sections"


class Ticket(BaseModel):
    order_id = IntegerField(null=False)
    section = ForeignKeyField(Section, backref="tickets")

    def to_dict(self):
        return model_to_dict(self)

    class Meta:
        table_name = "tickets"