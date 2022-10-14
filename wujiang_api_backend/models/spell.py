"""
Spell Model
"""
from wujiang_api_backend.db import db, ma


class Spell(db.Model):

    spell_id = db.Column(db.Integer, primary_key=True)
    spell_name = db.Column(db.String(100), unique=True)
    spell_description = db.Column(db.String(1000), default='')

    def __init__(self,
                 spell_id,
                 spell_name,
                 spell_description):
        self.spell_id = spell_id
        self.spell_name = spell_name
        self.spell_description = spell_description
        # TODO relationship


# Spell Schema
class SpellSchema(ma.Schema):
    class Meta:
        fields = {
            'spell_name',
            'spell_description'
        }
