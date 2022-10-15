from flask import Flask, request
from flask_restful import Api

from wujiang_api_backend.db import create_app
from wujiang_api_backend.resources.unit import \
    Units, \
    Unit


app = create_app()
api = Api(app)

api.add_resource(Units, '/units')
api.add_resource(Unit, '/unit')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
