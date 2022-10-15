"""
Unit Resource
"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort

from wujiang_api_backend.db import db
from wujiang_api_backend.models.unit import UnitModel, UnitSchema


class Units(Resource):
    units_schema = UnitSchema(many=True)

    @staticmethod
    def get():

        all_units = UnitModel.query.all()
        result = Units.units_schema.dump(all_units)
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
# todo add spells and properties here


class Unit(Resource):
    unit_schema = UnitSchema()

    def post(self):
        args = unit_post_args.parse_args()
        if db.session.query(UnitModel).filter(UnitModel.unit_name == args['unit_name']).all():
            abort(409, msg='Username already exists')
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
        db.session.add(unit)
        db.session.commit()
        return make_response(Unit.unit_schema.dump(unit), 201)
