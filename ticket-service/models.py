import time
import os
import sys
import bcrypt
from peewee import *


db = None

def initialize_database():
    global db
    if os.environ.get("DB"):
        db = SqliteDatabase(os.environ.get("DB"))
    else:
        sys.exit(1)


class BaseModel(Model):

    created_at = BigIntegerField(default=int(round(time.time() * 1000)))
    updated_at = BigIntegerField(default=int(round(time.time() * 1000)))

    class Meta:
        database = db

    def save(self, force_insert=False, only=None):
        self.updated_at = int(round(time.time() * 1000))
        return super(BaseModel, self).save(force_insert, only)


class User(BaseModel):
    username = CharField(max_length=100, null=False, unique=True, index=True)
    fullname = CharField(max_length=100, null=False, default="Anonymous")
    email = CharField(max_length=100, null=False, unique=True, index=True)
    password = CharField(max_length=100, null=False)
    address = CharField(max_length=255, null=False)

    def validate_password(self, password):
        return bcrypt.checkpw(password, self.password)

    def update_attr(self, params: dict):
        self.username = params["username"]
        self.fullname = params["fullname"]
        self.email = params["email"]
        self.address = params["address"]

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            "address": self.address
        }

    class Meta:
        table_name = "users"


class Partner(BaseModel):
    name = CharField(max_length=100, null=False, unique=True)
    address = CharField(max_length=255, null=False)
    email = CharField(max_length=100, null=False, unique=True)
    contact_number = CharField(max_length=20, null=False)

    class Meta:
        table_name = "partners"


class Event(BaseModel):
    name = CharField(max_length=100, null=False, unique=True, index=True)
    location = CharField(max_length=255, null=False)
    start_at = BigIntegerField(null=False)
    end_at = BigIntegerField(null=False)
    partner = ForeignKeyField(Partner, backref="events")

    class Meta:
        table_name = "events"


class Section(BaseModel):
    name = CharField(max_length=100, null=False)
    max_capacity = IntegerField(null=False)
    capacity = IntegerField(null=False)
    price = IntegerField(null=False)
    seat = BooleanField(null=False, default=False)
    event = ForeignKeyField(Event)

    class Meta:
        table_name = "sections"


class Ticket(BaseModel):
    section = ForeignKeyField(Section)
    owned_by = IntegerField(null=True, default=0)

    class Meta:
        table_name = "tickets"


class Order(BaseModel):
    status = CharField(max_length=20, null=False)
    total_price = BigIntegerField(null=False)
    user = ForeignKeyField(User)

    class Meta:
        table_name = "orders"


class OrderLine(BaseModel):
    event = ForeignKeyField(User)
    order = ForeignKeyField(Order, backref="order_lines")
    ticket = ForeignKeyField(Ticket)

    class Meta:
        table_name = "order_lines"
