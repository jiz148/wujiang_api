from flask_restful import Api

from wujiang_api_backend.db import create_app
from wujiang_api_backend.resources.unit import \
    Units, \
    Unit
from wujiang_api_backend.resources.spell import \
    Spells, \
    Spell
from wujiang_api_backend.resources.property import \
    Properties, \
    Property


app = create_app()
api = Api(app)

api.add_resource(Units, '/units')
api.add_resource(Unit, '/unit')
api.add_resource(Spells, '/spells')
api.add_resource(Spell, '/spell')
api.add_resource(Properties, '/properties')
api.add_resource(Property, '/property')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
