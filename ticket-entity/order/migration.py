from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from src.models import Ticket, Section, DatabaseManager


def drop_tables(db):
    db.drop_tables([Ticket, Section])


def create_tables(db):
    db.create_tables([Ticket, Section])


drop_tables(DatabaseManager.get_database())
create_tables(DatabaseManager.get_database())
