"""
Spell Resource
"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort

from wujiang_api_backend.db import db
from wujiang_api_backend.models.spell import SpellModel, SpellSchema


class Spells(Resource):

    @staticmethod
    def get():

        all_spells = SpellModel.query.all()
        result = SpellSchema(many=True).dump(all_spells)
        return jsonify(result)


spell_post_args = reqparse.RequestParser()
spell_post_args.add_argument("spell_name", type=str, required=True)
spell_post_args.add_argument("spell_description", type=str, required=True)


class Spell(Resource):

    @staticmethod
    def post():
        args = spell_post_args.parse_args()
        if db.session.query(SpellModel).filter(SpellModel.spell_name == args['spell_name']).all():
            abort(409, msg='spell name already exists')

        spell = SpellModel(
            spell_name=args['spell_name'],
            spell_description=args['spell_description'],
        )

        db.session.add(spell)
        db.session.commit()
        return make_response(SpellSchema().dump(spell), 201)
