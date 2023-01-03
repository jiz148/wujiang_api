from flask_restful import Api

from wujiang_api_backend.db import create_app
from wujiang_api_backend.resources.unit import \
    Units, \
    UnitsBySpell, \
    UnitsByProperty, \
    UnitDetail, \
    UnitAdd, \
    UnitUpdate, \
    UnitDelete
from wujiang_api_backend.resources.spell import \
    Spells, \
    Spell
from wujiang_api_backend.resources.property import \
    Properties, \
    Property


app = create_app()
api = Api(app)

api.add_resource(Units, '/unit/getUnitList')
api.add_resource(UnitsBySpell, '/unit/getUnitListBySpell')
api.add_resource(UnitsByProperty, '/unit/getUnitListByProperty')
api.add_resource(UnitDetail, '/unit/getUnitDetail')
api.add_resource(UnitAdd, '/unit/addUnit')
api.add_resource(UnitDelete, '/unit/deleteUnit')
api.add_resource(UnitUpdate, '/unit/editUnit')
api.add_resource(Spells, '/spell/getSpellList')
api.add_resource(Spell, '/spell')
api.add_resource(Properties, '/properties')
api.add_resource(Property, '/property')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
