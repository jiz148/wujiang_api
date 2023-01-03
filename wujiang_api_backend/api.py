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
    SpellsByUnit, \
    Spell, \
    SpellDetail, \
    SpellUpdate, \
    SpellDelete
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
api.add_resource(SpellsByUnit, '/spell/getSpellListByUnit')
api.add_resource(SpellDetail, '/spell/getSpellDetail')
api.add_resource(Spell, '/spell/addSpell')
api.add_resource(SpellUpdate, '/spell/editSpell')
api.add_resource(SpellDelete, '/spell/deleteSpell')
api.add_resource(Properties, '/properties')
api.add_resource(Property, '/property')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
