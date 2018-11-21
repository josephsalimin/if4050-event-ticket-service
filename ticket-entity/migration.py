from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


import auth.models
import event.models
import order.models
import partner.models
import ticket.models
import user.models


def refresh_auth():
    db = auth.models.DatabaseManager.get_database()
    db.drop_tables([auth.models.AuthService])
    db.create_tables([auth.models.AuthService])


def refresh_event():
    db = event.models.DatabaseManager.get_database()
    db.drop_tables([event.models.Event])
    db.create_tables([event.models.Event])


def refresh_order():
    db = order.models.DatabaseManager.get_database()
    db.drop_tables([order.models.ReservedTicket,order.models.Order])
    db.create_tables([order.models.ReservedTicket, order.models.Order])


def refresh_partner():
    db = partner.models.DatabaseManager.get_database()
    db.drop_tables([partner.models.Partner])
    db.create_tables([partner.models.Partner])


def refresh_ticket():
    db = ticket.models.DatabaseManager.get_database()
    db.drop_tables([ticket.models.Ticket, ticket.models.Section])
    db.create_tables([ticket.models.Ticket, ticket.models.Section])


def refresh_user():
    db = user.models.DatabaseManager.get_database()
    db.drop_tables([user.models.User])
    db.create_tables([user.models.User])
