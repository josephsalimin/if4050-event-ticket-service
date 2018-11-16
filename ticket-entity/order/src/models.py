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


class Order(BaseModel):
    status = CharField(max_length=20, null=False)
    total_price = BigIntegerField(null=False)
    user_id = IntegerField(null=False)

    def to_dict(self):
        return model_to_dict(self, recurse=True)

    class Meta:
        table_name = "orders"


class ReservedTicket(BaseModel):
    section_id = IntegerField(null=False)
    quantity = IntegerField(null=False)
    order_id = IntegerField(null=False)

    def to_dict(self):
        return model_to_dict(self, recurse=True)
    
    class Meta:
        table_name = "reserved_tickets"