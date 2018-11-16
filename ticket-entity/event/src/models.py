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


class Event(BaseModel):
    name = CharField(max_length=100, null=False, unique=True, index=True)
    description = CharField(max_length=255, null=False)
    location = CharField(max_length=255, null=False)
    start_at = BigIntegerField(null=False)
    end_at = BigIntegerField(null=False)
    partner_id = IntegerField(null=False)

    def to_dict(self):
        return model_to_dict(self)

    def validate(self):
        return int(round(time.time())) > self.end_at

    def update_attr(self, name, description, location, start_at, end_at):
        self.name = name
        self.description = description
        self.location = location
        self.start_at = start_at
        self.end_at = end_at

    class Meta:
        table_name = "events"
