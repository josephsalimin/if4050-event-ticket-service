from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from src.models import Partner, DatabaseManager


def drop_tables(db):
    db.drop_tables([Partner])


def create_tables(db):
    db.create_tables([Partner])


drop_tables(DatabaseManager.get_database())
create_tables(DatabaseManager.get_database())
