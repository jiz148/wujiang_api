"""
Unit Model
"""
from wujiang_api_backend.db import db, ma


class Unit(db.Model):
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(100), unique=True)
    level = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    range = db.Column(db.Integer)
    magic = db.Column(db.Integer)
    is_wujiang = db.Column(db.Boolean, defalut=True)

    def __init__(self,
                 unit_id,
                 unit_name,
                 level,
                 attack,
                 defence,
                 speed,
                 range,
                 magic,
                 is_wujiang
                 ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.level = level
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.range = range
        self.magic = magic
        self.is_wujiang = is_wujiang
        # TODO relationship


# Unit Schema
class UnitSchema(ma.Schema):
    class Meta:
        fields = {
            'unit_id',
            'unit_name',
            'level',
            'attack',
            'defence',
            'speed',
            'range',
            'magic',
            'is_wujiang'
        }
