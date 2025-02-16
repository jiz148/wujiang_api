"""
Unit Model
"""
from wujiang_api_backend.db import db, ma
from wujiang_api_backend.models.spell import SpellModel, SpellSchema
from wujiang_api_backend.models.property import PropertyModel, PropertySchema


class UnitModel(db.Model):
    __tablename__ = 'unit'

    # many-to-many relationships
    unit_has_spell = db.Table(
        'unit_has_spell',
        db.Column('unit_id', db.Integer, db.ForeignKey('unit.unit_id')),
        db.Column('spell_id', db.Integer, db.ForeignKey('spell.spell_id'))
    )
    unit_has_property = db.Table(
        'unit_has_property',
        db.Column('unit_id', db.Integer, db.ForeignKey('unit.unit_id')),
        db.Column('property_id', db.Integer, db.ForeignKey('property.property_id'))
    )

    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(100), unique=True)
    race = db.Column(db.String(100), unique=True)
    level = db.Column(db.Integer)
    build_slots = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    range = db.Column(db.Integer)
    magic = db.Column(db.Integer)
    is_wujiang = db.Column(db.Boolean, default=True)
    spell = db.relationship(SpellModel, secondary=unit_has_spell, backref='units')
    property = db.relationship(PropertyModel, secondary=unit_has_property, backref='units')


# Unit Schema
class UnitSchema(ma.Schema):
    class Meta:
        model = UnitModel
        fields = [
            'unit_id',
            'unit_name',
            'level',
            'build_slots',
            'attack',
            'defence',
            'speed',
            'range',
            'magic',
            'is_wujiang',
            'spell',
            'property',
        ]

    spell = ma.Nested(SpellSchema(many=True))
    property = ma.Nested(PropertySchema(many=True))
