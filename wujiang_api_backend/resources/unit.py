"""
Unit Resource
"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort

from wujiang_api_backend.db import db
from wujiang_api_backend.models.unit import UnitModel, UnitSchema
from wujiang_api_backend.models.spell import SpellModel
from wujiang_api_backend.models.property import PropertyModel


class Units(Resource):

    @staticmethod
    def get():

        all_units = UnitModel.query.all()
        result = UnitSchema(many=True).dump(all_units)
        return jsonify(result)


unit_post_args = reqparse.RequestParser()
unit_post_args.add_argument("unit_name", type=str, required=True)
unit_post_args.add_argument("level", type=int, required=True)
unit_post_args.add_argument("attack", type=int, required=True)
unit_post_args.add_argument("defence", type=int, required=True)
unit_post_args.add_argument("speed", type=int, required=True)
unit_post_args.add_argument("range", type=int, required=True)
unit_post_args.add_argument("magic", type=int, required=True)
unit_post_args.add_argument("is_wujiang", type=bool, required=True)
unit_post_args.add_argument("spells", type=int, action='append', required=True)
unit_post_args.add_argument("properties", type=int, action='append', required=True)


class Unit(Resource):

    def post(self):
        args = unit_post_args.parse_args()
        if db.session.query(UnitModel).filter(UnitModel.unit_name == args['unit_name']).all():
            abort(409, msg='Username already exists')
        # check spell availability
        for spell_id in args['spells']:
            if not db.session.query(SpellModel).filter(SpellModel.spell_id == spell_id).all():
                abort(404, msg='Spell does not exist')

        # check property availability
        for property_id in args['properties']:
            if not db.session.query(PropertyModel).filter(PropertyModel.property_id == property_id).all():
                abort(404, msg='Property does not exist')

        unit = UnitModel(
            unit_name=args['unit_name'],
            level=args['level'],
            attack=args['attack'],
            defence=args['defence'],
            speed=args['speed'],
            range=args['range'],
            magic=args['magic'],
            is_wujiang=args['is_wujiang'],
        )
        # add spells
        for spell_id in set(args['spells']):
            spell = db.session.query(SpellModel).filter(SpellModel.spell_id == spell_id).first()
            unit.spell.append(spell)
        for property_id in set(args['properties']):
            property = db.session.query(PropertyModel).filter(PropertyModel.property_id == property_id).first()
            unit.property.append(property)

        db.session.add(unit)
        db.session.commit()
        return make_response(UnitSchema().dump(unit), 201)
