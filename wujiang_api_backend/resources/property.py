"""
Property Resource
"""
from flask import jsonify, make_response, request
from flask_restful import Resource, reqparse, abort
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

from wujiang_api_backend.db import db
from wujiang_api_backend.models.property import PropertyModel, PropertySchema
from wujiang_api_backend.models.unit import UnitModel


class Properties(Resource):

    @staticmethod
    def get():
        args = request.args
        num_of_units = db.session.query(UnitModel).count() if db.session.query(UnitModel).count() else 1
        page_num = int(args['pageNum'])
        page_size = int(args.get('pageSize', num_of_units))

        sort_name = args.get('sortName')
        sort_order = args.get('sortOrder')
        name = args.get('name')

        results = db.session.query(PropertyModel)

        if sort_name:
            sort_order = 'desc' if sort_order == 'descend' else 'asc'
            order_text = sort_name + ' ' + sort_order
            results = results.order_by(text(order_text))

        if name:
            name = '%' + name + '%'
            results = results.filter(PropertyModel.property_name.like(name))

        try:
            results = results.paginate(page=page_num, per_page=page_size)
        except OperationalError:
            abort(400, msg='sql query error')
        properties = PropertySchema(many=True).dump(results)
        data = {
            'total': len(properties),
            'list': properties
        }
        response = {
            'code': 200,
            'data': data
        }
        return jsonify(response)


property_post_args = reqparse.RequestParser()
property_post_args.add_argument("name", type=str, required=True)
property_post_args.add_argument("description", type=str, required=True)


class Property(Resource):

    @staticmethod
    def post():
        args = property_post_args.parse_args()
        if db.session.query(PropertyModel).filter(PropertyModel.property_name == args['name']).all():
            abort(409, msg='property name already exists')

        property = PropertyModel(
            property_name=args['name'],
            property_description=args['description'],
        )

        db.session.add(property)
        db.session.commit()
        response = {
            'code': 201,
            'data': PropertySchema().dump(property)
        }
        return make_response(response, 201)


class PropertiesByUnit(Resource):

    @staticmethod
    def get():
        args = request.args
        unit_id = args['unitId']
        unit = db.session.query(UnitModel).filter(UnitModel.unit_id == unit_id).first()
        if not unit:
            abort(404, msg='unit does not exist')
        results = unit.property
        properties = PropertySchema(many=True).dump(results)
        response = {
            'code': 200,
            'data': {
                'list': properties
            }
        }
        return jsonify(response)


class PropertyDetail(Resource):

    @staticmethod
    def get():
        args = request.args
        property_id = args['id']
        property = db.session.query(PropertyModel).filter(PropertyModel.property_id == property_id).first()
        if not property:
            abort(404, msg='Property does not exist')
        response = {
            'code': 200,
            'data': PropertySchema().dump(property)
        }
        return jsonify(response)


property_put_args = reqparse.RequestParser()
property_put_args.add_argument("property_id", type=str, required=True)
property_put_args.add_argument("name", type=str, required=True)
property_put_args.add_argument("description", type=str, required=True)


class PropertyUpdate(Resource):

    @staticmethod
    def put():
        args = property_put_args.parse_args()
        # check property availability
        property = db.session.query(PropertyModel).filter(PropertyModel.property_id == args['property_id']).first()
        if not property:
            abort(404, msg='property does not exist')
        original_name = property.property_name
        if original_name != args['name']:
            # check property name availability
            if db.session.query(PropertyModel).filter(PropertyModel.property_name == args['name']).all():
                abort(409, msg='property name already exists')
        property.property_name = args['name']
        property.property_description = args['description']

        db.session.commit()
        response = {
            'code': 201,
            'data': PropertySchema().dump(property)
        }
        return make_response(response, 201)


class PropertyDelete(Resource):

    def delete(self):
        args = request.args
        if not db.session.query(PropertyModel).filter(PropertyModel.property_id == args['id']).first():
            abort(404, msg='property does not exist')
        try:
            db.session.query(PropertyModel).filter(PropertyModel.property_id == args['id']).delete()
        except:
            abort(404, msg="error happened in delete")
        db.session.commit()
