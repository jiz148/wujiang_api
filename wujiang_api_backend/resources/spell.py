"""
Spell Resource
"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

from wujiang_api_backend.db import db
from wujiang_api_backend.models.spell import SpellModel, SpellSchema
from wujiang_api_backend.models.unit import UnitModel


spells_get_args = reqparse.RequestParser()
spells_get_args.add_argument("pageNum", type=int, required=True)
spells_get_args.add_argument("pageSize", type=int, required=True)
spells_get_args.add_argument("sortName", type=str, required=False)
spells_get_args.add_argument("sortOrder", type=str, required=False)
spells_get_args.add_argument("name", type=str, required=False)


class Spells(Resource):

    @staticmethod
    def get():
        args = spells_get_args.parse_args()
        page_num = args['pageNum']
        page_size = args['pageSize']

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
        response = {
            'total': len(spells),
            'list': spells
        }
        return jsonify(response)


spell_post_args = reqparse.RequestParser()
spell_post_args.add_argument("name", type=str, required=True)
spell_post_args.add_argument("description", type=str, required=True)


class Spell(Resource):

    @staticmethod
    def post():
        args = spell_post_args.parse_args()
        if db.session.query(SpellModel).filter(SpellModel.spell_name == args['name']).all():
            abort(409, msg='spell name already exists')

        spell = SpellModel(
            spell_name=args['name'],
            spell_description=args['description'],
        )

        db.session.add(spell)
        db.session.commit()
        return make_response(SpellSchema().dump(spell), 201)


spell_by_unit_get_args = reqparse.RequestParser()
spell_by_unit_get_args.add_argument("unitId", type=str, required=True)


class SpellsByUnit(Resource):

    @staticmethod
    def get():
        args = spell_by_unit_get_args.parse_args()
        unit_id = args['unitId']
        unit = db.session.query(UnitModel).filter(UnitModel.unit_id == unit_id).first()
        if not unit:
            abort(404, msg='unit does not exist')
        results = unit.spell
        spells = SpellSchema(many=True).dump(results)
        response = {
            'list': spells
        }
        return jsonify(response)


spell_detail_get_args = reqparse.RequestParser()
spell_detail_get_args.add_argument("id", type=str, required=True)


class SpellDetail(Resource):

    @staticmethod
    def get():
        args = spell_detail_get_args.parse_args()
        spell_id = args['id']
        spell = db.session.query(SpellModel).filter(SpellModel.spell_id == spell_id).first()
        if not spell:
            abort(404, msg='Spell does not exist')
        return jsonify(SpellSchema().dump(spell))
