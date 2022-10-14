import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# init db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# init ma

ma = Marshmallow(app)


def create_db():
    from wujiang_api_backend.models.unit import Unit
    from wujiang_api_backend.models.spell import Spell
    from wujiang_api_backend.models.property import Property
    with app.app_context():
        db.create_all()
