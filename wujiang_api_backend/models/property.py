"""
Property Model
"""
from wujiang_api_backend.db import db, ma


class Property(db.Model):
    property_id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(100), unique=True)
    property_description = db.Column(db.String(1000), default='')
    
    def __init__(self,
                 property_id,
                 property_name,
                 property_description):
        self.property_id = property_id
        self.property_name = property_name
        self.property_description = property_description
        # TODO relationship


# Property Schema
class PropertySchema(ma.Schema):
    class Meta:
        fields = {
            'property_name',
            'property_description'
        }
