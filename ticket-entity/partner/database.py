import os
import sys
from peewee import SqliteDatabase


class DatabaseManager:

    __sqlite_db = None

    @classmethod
    def initialize_database(cls):
        if cls.__sqlite_db is not None:
            return
        if os.environ.get("PARTNER_DB"):
            cls.__sqlite_db = SqliteDatabase(os.environ.get("PARTNER_DB"), pragmas={
                'journal_mode': 'wal',
                'cache_size': -1024 * 64})
        else:
            sys.exit(1)

    @classmethod
    def get_database(cls):
        if cls.__sqlite_db is None:
            cls.initialize_database()
        return cls.__sqlite_db
