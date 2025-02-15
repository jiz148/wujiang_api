"""
Unit Resource
"""
from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse, abort
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

from wujiang_api_backend.db import db
from wujiang_api_backend.models.unit import UnitModel, UnitSchema
from wujiang_api_backend.models.spell import SpellModel
from wujiang_api_backend.models.property import PropertyModel


class Units(Resource):

    @staticmethod
    def get():
        args = request.args
        num_of_units = db.session.query(UnitModel).count() if db.session.query(UnitModel).count() else 1
        page_num = int(args.get('pageNum', 1))
        page_size = int(args.get('pageSize', num_of_units))

        sort_name = args.get('sortName')
        sort_order = args.get('sortOrder')
        name = args.get('name')

        results = db.session.query(UnitModel)

        if sort_name:
            sort_order = 'desc' if sort_order == 'descend' else 'asc'
            order_text = sort_name + ' ' + sort_order
            results = results.order_by(text(order_text))

        if name:
            name = '%' + name + '%'
            results = results.filter(UnitModel.unit_name.like(name))
        count = results.count()

        try:
            results = results.paginate(page=page_num, per_page=page_size)
        except OperationalError:
            abort(400, msg='sql query error')
        units = UnitSchema(many=True).dump(results)
        data = {
            'total': count,
            'list': units
        }
        response = {
            'code': 200,
            'data': data
        }
        return jsonify(response)


class UnitsBySpell(Resource):

    @staticmethod
    def get():
        args = request.args
        spell_id = args['spellId']
        spell = db.session.query(SpellModel).filter(SpellModel.spell_id == spell_id).first()
        results = db.session.query(UnitModel)\
            .filter(UnitModel.spell.contains(spell)).all()
        units = UnitSchema(many=True).dump(results)
        response = {
            'code': 200,
            'data': {
                'list': units
            }
        }
        return jsonify(response)


class UnitsByProperty(Resource):

    @staticmethod
    def get():
        args = request.args
        property_id = args['propertyId']
        property = db.session.query(PropertyModel).filter(PropertyModel.property_id == property_id).first()
        results = db.session.query(UnitModel)\
            .filter(UnitModel.property.contains(property)).all()
        units = UnitSchema(many=True).dump(results)
        response = {
            'code': 200,
            'data': {
                'list': units
            }
        }
        return jsonify(response)


class UnitDetail(Resource):

    @staticmethod
    def get():
        args = request.args
        unit_id = args['id']
        unit = db.session.query(UnitModel).filter(UnitModel.unit_id == unit_id).first()
        if not unit:
            abort(404, msg='Unit does not exist')
        response = {
            'code': 200,
            'data': UnitSchema().dump(unit),
        }
        return jsonify(response)


unit_post_args = reqparse.RequestParser()
unit_post_args.add_argument("unit_name", type=str, required=True)
unit_post_args.add_argument("level", type=int, required=True)
unit_post_args.add_argument("type", type=str, required=True)
unit_post_args.add_argument("race", type=str, required=True)
unit_post_args.add_argument("role", type=str, required=True)
unit_post_args.add_argument("build_slots", type=int, required=True)
unit_post_args.add_argument("attack", type=int, required=True)
unit_post_args.add_argument("defence", type=int, required=True)
unit_post_args.add_argument("speed", type=int, required=True)
unit_post_args.add_argument("range", type=int, required=True)
unit_post_args.add_argument("magic", type=int, required=True)
unit_post_args.add_argument("is_wujiang", type=bool, required=True)
unit_post_args.add_argument("spells", type=int, action='append', default=list)
unit_post_args.add_argument("properties", type=int, action='append', default=list)


class UnitAdd(Resource):

    @staticmethod
    def post():
        args = unit_post_args.parse_args()
        if db.session.query(UnitModel).filter(UnitModel.unit_name == args['unit_name']).all():
            abort(409, msg='unit name already exists')
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
            type=args['type'],
            race=args['race'],
            build_slots=args['build_slots'],
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
        response = {
            'code': 201,
            'data': UnitSchema().dump(unit),
        }
        return make_response(response, 201)


unit_update_args = reqparse.RequestParser()
unit_update_args.add_argument("unit_id", type=str, required=True)
unit_update_args.add_argument("unit_name", type=str, required=False)
unit_update_args.add_argument("level", type=int, required=False)
unit_update_args.add_argument("type", type=str, required=True)
unit_update_args.add_argument("race", type=str, required=True)
unit_update_args.add_argument("role", type=str, required=True)
unit_update_args.add_argument("build_slots", type=int, required=True)
unit_update_args.add_argument("attack", type=int, required=False)
unit_update_args.add_argument("defence", type=int, required=False)
unit_update_args.add_argument("speed", type=int, required=False)
unit_update_args.add_argument("range", type=int, required=False)
unit_update_args.add_argument("magic", type=int, required=False)
unit_update_args.add_argument("is_wujiang", type=bool, required=False)
unit_update_args.add_argument("spells", type=int, action='append', required=False)
unit_update_args.add_argument("properties", type=int, action='append', required=False)


class UnitUpdate(Resource):
    
    def put(self):
        args = unit_update_args.parse_args()
        # check unit availability
        unit = db.session.query(UnitModel).filter(UnitModel.unit_id == args['unit_id']).first()
        if not unit:
            abort(404, msg='unit does not exist')

        unit_name = args.get('unit_name')
        level = args.get('level')
        type = args.get('type')
        race = args.get('race')
        role = args.get('role')
        build_slots = args.get('build_slots')
        attack = args.get('attack')
        defence = args.get('defence')
        speed = args.get('speed')
        unit_range = args.get('range')
        magic = args.get('magic')
        is_wujiang = args.get('is_wujiang')
        spells = args.get('spells')
        properties = args.get('properties')

        if unit_name:
            original_name = unit.unit_name
            if unit_name != original_name:
                # check new name availability
                if db.session.query(UnitModel).filter(UnitModel.unit_name == args['unit_name']).all():
                    abort(404, msg='unit name already exists')
        if spells:
            # check spell availability
            for spell_id in spells:
                if not db.session.query(SpellModel).filter(SpellModel.spell_id == spell_id).all():
                    abort(404, msg='Spell does not exist')

        if properties:
            # check property availability
            for property_id in properties:
                if not db.session.query(PropertyModel).filter(PropertyModel.property_id == property_id).all():
                    abort(404, msg='Property does not exist')

        # update unit
        if unit_name:
            unit.unit_name = unit_name
        if level:
            unit.level = level
        if type:
            unit.type = type
        if role:
            unit.role = role
        if race:
            unit.race = race
        if build_slots:
            unit.build_slots = build_slots
        if attack:
            unit.attack = attack
        if defence:
            unit.defence = defence
        if speed:
            unit.speed = speed
        if unit_range:
            unit.range = unit_range
        if magic:
            unit.magic = magic
        if is_wujiang:
            unit.is_wujiang = is_wujiang
        # add spells
        if spells:
            unit.spell = []
            for spell_id in set(spells):
                spell = db.session.query(SpellModel).filter(SpellModel.spell_id == spell_id).first()
                unit.spell.append(spell)
        if properties:
            unit.property = []
            for property_id in set(properties):
                property = db.session.query(PropertyModel).filter(PropertyModel.property_id == property_id).first()
                unit.property.append(property)

        db.session.commit()
        response = {
            'code': 201,
            'data': UnitSchema().dump(unit),
        }
        return make_response(response, 201)


class UnitDelete(Resource):

    def delete(self):
        args = request.args
        if not db.session.query(UnitModel).filter(UnitModel.unit_id == args['id']).first():
            abort(404, msg='unit does not exist')
        try:
            db.session.query(UnitModel).filter(UnitModel.unit_id == args['id']).delete()
        except:
            abort(404, msg="error happened in delete")
        db.session.commit()
