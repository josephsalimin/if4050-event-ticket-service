import os
from flask import Flask
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from auth.routes import auth
from event.routes import event
from order.routes import order
from partner.routes import partner
from ticket.routes import ticket, ticket_section
from user.routes import user


app = Flask(__name__)
app.register_blueprint(event, url_prefix="/event")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(order, url_prefix="/order")
app.register_blueprint(partner, url_prefix="/partner")
app.register_blueprint(ticket_section, url_prefix="/ticket_section")
app.register_blueprint(ticket, url_prefix="/ticket")
app.register_blueprint(user, url_prefix="/user")


if __name__ == '__main__':
    app.run(port=os.environ.get('PORT'), debug=True)
