from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from src.models import AuthService, DatabaseManager


def drop_tables(db):
    db.drop_tables([AuthService])


def create_tables(db):
    db.create_tables([AuthService])


drop_tables(DatabaseManager.get_database())
create_tables(DatabaseManager.get_database())
