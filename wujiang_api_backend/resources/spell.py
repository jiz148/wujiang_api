"""
Spell Resource
"""
from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse, abort
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

from wujiang_api_backend.db import db
from wujiang_api_backend.models.spell import SpellModel, SpellSchema
from wujiang_api_backend.models.unit import UnitModel


class Spells(Resource):

    @staticmethod
    def get():
        args = request.args
        num_of_units = db.session.query(UnitModel).count() if db.session.query(UnitModel).count() else 1
        page_num = int(args['pageNum'])
        page_size = int(args.get('pageSize', num_of_units))

        sort_name = args.get('sortName')
        sort_order = args.get('sortOrder')
        name = args.get('name')

        results = db.session.query(SpellModel)

        if sort_name:
            sort_order = 'desc' if sort_order == 'descend' else 'asc'
            order_text = sort_name + ' ' + sort_order
            results = results.order_by(text(order_text))

        if name:
            name = '%' + name + '%'
            results = results.filter(SpellModel.spell_name.like(name))

        try:
            results = results.paginate(page=page_num, per_page=page_size)
        except OperationalError:
            abort(400, msg='sql query error')
        spells = SpellSchema(many=True).dump(results)
        data = {
            'total': len(spells),
            'list': spells
        }
        response = {
            'code': 200,
            'data': data
        }
        return jsonify(response)


spell_post_args = reqparse.RequestParser()
spell_post_args.add_argument("name", type=str, required=True)
spell_post_args.add_argument("cost", type=int, required=True)
spell_post_args.add_argument("description", type=str, required=True)


class Spell(Resource):

    @staticmethod
    def post():
        args = spell_post_args.parse_args()
        if db.session.query(SpellModel).filter(SpellModel.spell_name == args['name']).all():
            abort(409, msg='spell name already exists')

        spell = SpellModel(
            spell_name=args['name'],
            spell_cost=args['cost'],
            spell_description=args['description'],
        )

        db.session.add(spell)
        db.session.commit()
        response = {
            'code': 201,
            'data': SpellSchema().dump(spell)
        }
        return make_response(response, 201)


class SpellsByUnit(Resource):

    @staticmethod
    def get():
        args = request.args
        unit_id = args['unitId']
        unit = db.session.query(UnitModel).filter(UnitModel.unit_id == unit_id).first()
        if not unit:
            abort(404, msg='unit does not exist')
        results = unit.spell
        spells = SpellSchema(many=True).dump(results)
        response = {
            'code': 200,
            'data': {
                'list': spells
            }
        }
        return jsonify(response)


class SpellDetail(Resource):

    @staticmethod
    def get():
        args = request.args
        spell_id = args['id']
        spell = db.session.query(SpellModel).filter(SpellModel.spell_id == spell_id).first()
        if not spell:
            abort(404, msg='Spell does not exist')
        response = {
            'code': 200,
            'data': SpellSchema().dump(spell)
        }
        return jsonify(response)


spell_put_args = reqparse.RequestParser()
spell_put_args.add_argument("spell_id", type=str, required=True)
spell_put_args.add_argument("name", type=str, required=True)
spell_put_args.add_argument("cost", type=int, required=True)
spell_put_args.add_argument("description", type=str, required=True)


class SpellUpdate(Resource):

    @staticmethod
    def put():
        args = spell_put_args.parse_args()
        # check spell availability
        spell = db.session.query(SpellModel).filter(SpellModel.spell_id == args['spell_id']).first()
        if not spell:
            abort(404, msg='spell does not exist')
        original_name = spell.spell_name
        if original_name != args['name']:
            # check spell name availability
            if db.session.query(SpellModel).filter(SpellModel.spell_name == args['name']).all():
                abort(409, msg='spell name already exists')
        spell.spell_name = args['name']
        spell.spell_cost = args['cost']
        spell.spell_description = args['description']

        db.session.commit()
        response = {
            'code': 201,
            'data': SpellSchema().dump(spell)
        }
        return make_response(response, 201)


class SpellDelete(Resource):

    def delete(self):
        args = request.args
        if not db.session.query(SpellModel).filter(SpellModel.spell_id == args['id']).first():
            abort(404, msg='spell does not exist')
        try:
            db.session.query(SpellModel).filter(SpellModel.spell_id == args['id']).delete()
        except:
            abort(404, msg="error happened in delete")
        db.session.commit()
