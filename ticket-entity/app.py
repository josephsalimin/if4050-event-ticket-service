import os
from flask import Flask
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


from auth.routes import auth
# from event.routes import event


app = Flask(__name__)
with app.app_context():
    app.register_blueprint(auth, url_prefix="/auth")


if __name__ == '__main__':
    app.run(port=os.environ.get('PORT'), debug=True)
