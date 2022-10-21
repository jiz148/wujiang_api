"""
Property Resource
"""
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort

from wujiang_api_backend.db import db
from wujiang_api_backend.models.property import PropertyModel, PropertySchema


class Properties(Resource):

    @staticmethod
    def get():

        all_properties = PropertyModel.query.all()
        result = PropertySchema(many=True).dump(all_properties)
        return jsonify(result)


property_post_args = reqparse.RequestParser()
property_post_args.add_argument("property_name", type=str, required=True)
property_post_args.add_argument("property_description", type=str, required=True)


class Property(Resource):

    @staticmethod
    def post():
        args = property_post_args.parse_args()
        if db.session.query(PropertyModel).filter(PropertyModel.property_name == args['property_name']).all():
            abort(409, msg='property name already exists')

        property = PropertyModel(
            property_name=args['property_name'],
            property_description=args['property_description'],
        )

        db.session.add(property)
        db.session.commit()
        return make_response(PropertySchema().dump(property), 201)
