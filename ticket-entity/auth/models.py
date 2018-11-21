import time
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


class AuthService(BaseModel):
    name = CharField(max_length=100, null=False, unique=True, index=True)
    auth_type = CharField(max_length=100, null=False)
    refresh_token = CharField(max_length=255, null=False, default="")
    auth_token = CharField(max_length=255, null=False, default="")
    partner_id = IntegerField(null=False)

    class Meta:
        table_name = 'auth'

    def to_dict(self):
        return model_to_dict(self)
