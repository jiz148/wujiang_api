"""
Spell Model
"""
from wujiang_api_backend.db import db, ma


class SpellModel(db.Model):
    __tablename__ = 'spell'

    spell_id = db.Column(db.Integer, primary_key=True)
    spell_name = db.Column(db.String(100), unique=True)
    spell_description = db.Column(db.String(1000), default='')


# Spell Schema
class SpellSchema(ma.Schema):
    class Meta:
        model = SpellModel
        fields = [
            'spell_name',
            'spell_description'
        ]
