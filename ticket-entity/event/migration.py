from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from src.models import Event, DatabaseManager


def drop_tables(db):
    db.drop_tables([Event])


def create_tables(db):
    db.create_tables([Event])


drop_tables(DatabaseManager.get_database())
create_tables(DatabaseManager.get_database())
