import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# init db
db_path = os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)


def create_app():
    with app.app_context():
        if not os.path.exists(db_path):
            create_db()
    return app


def create_db():
    from wujiang_api_backend.models.unit import UnitModel
    from wujiang_api_backend.models.spell import SpellModel
    from wujiang_api_backend.models.property import PropertyModel

    db.create_all()
