from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


import auth.models
import event.models


def refresh_auth():
    db = auth.models.DatabaseManager.get_database()
    db.drop_tables([auth.models.AuthService])
    db.create_tables([auth.models.AuthService])


def refresh_event():
    db = event.models.DatabaseManager.get_database()
    db.drop_tables([event.models.Event])
    db.create_tables([event.models.Event])