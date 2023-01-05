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
    PropertiesByUnit, \
    Property, \
    PropertyDetail, \
    PropertyUpdate, \
    PropertyDelete


app = create_app()
api = Api(app)

api.add_resource(Units, '/wujiang/unit/getUnitList')
api.add_resource(UnitsBySpell, '/wujiang/unit/getUnitListBySpell')
api.add_resource(UnitsByProperty, '/wujiang/unit/getUnitListByProperty')
api.add_resource(UnitDetail, '/wujiang/unit/getUnitDetail')
api.add_resource(UnitAdd, '/wujiang/unit/addUnit')
api.add_resource(UnitDelete, '/wujiang/unit/deleteUnit')
api.add_resource(UnitUpdate, '/wujiang/unit/editUnit')
api.add_resource(Spells, '/wujiang/spell/getSpellList')
api.add_resource(SpellsByUnit, '/wujiang/spell/getSpellListByUnit')
api.add_resource(SpellDetail, '/wujiang/spell/getSpellDetail')
api.add_resource(Spell, '/wujiang/spell/addSpell')
api.add_resource(SpellUpdate, '/wujiang/spell/editSpell')
api.add_resource(SpellDelete, '/wujiang/spell/deleteSpell')
api.add_resource(Properties, '/wujiang/property/getPropertyList')
api.add_resource(PropertiesByUnit, '/wujiang/property/getPropertyListByUnit')
api.add_resource(PropertyDetail, '/wujiang/property/getPropertyDetail')
api.add_resource(Property, '/wujiang/property/addProperty')
api.add_resource(PropertyUpdate, '/wujiang/property/editProperty')
api.add_resource(PropertyDelete, '/wujiang/property/deleteProperty')


if __name__ == '__main__':
    app.run(debug=True, port=3001)
