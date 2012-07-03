from cortex_client.api.resource import Resource
from cortex_client.api.collection import Collection
from cortex_client.api.parameters import ParameterFactory

class FlavorCollection(Collection):
    def __init__(self, api):
        super(FlavorCollection, self).__init__("flavors/", api)

    def _new_resource(self, json_data):
        res = Flavor(self, json_data)
        return res

class Flavor(Resource):
    def __init__(self, collection, json_data = None):
        super(Flavor, self).__init__(collection, json_data)

    def get_name(self):
        return self._get_field("name")

    def get_parameters(self):
        return self._get_list_field("parameters", ParameterFactory(self._collection))

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Parameters:"
        for p in self.get_parameters():
            p._show(indent + 2)

class FlavorFactory(object):
    def __init__(self, collection = None):
        self._collection = collection

    def new_object(self, json_data):
        return Flavor(self._collection, json_data)
