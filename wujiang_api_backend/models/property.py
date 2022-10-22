"""
Property Model
"""
from wujiang_api_backend.db import db, ma


class PropertyModel(db.Model):
    __tablename__ = 'property'

    property_id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(100), unique=True)
    property_description = db.Column(db.String(1000), default='')


# Property Schema
class PropertySchema(ma.Schema):
    class Meta:
        model = PropertyModel
        fields = [
            'property_id',
            'property_name',
            'property_description'
        ]
