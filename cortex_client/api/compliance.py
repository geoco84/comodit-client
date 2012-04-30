# coding: utf-8
from cortex_client.api.collection import Collection
from cortex_client.api.resource import Resource

class ComplianceError(Resource):
    def _get_path(self):
        return self._collection.get_path() + self.get_error_collection() + "/" + self.get_id()

    def get_error_collection(self):
        return self._get_field("collection")

    def get_id(self):
        return self._get_field("id")

    def _show(self, indent = 0):
        col = self.get_error_collection()
        print "Collection:", col
        print "Id:", self.get_id()

class ComplianceCollection(Collection):
    def _new_resource(self, json_data):
        return ComplianceError(self, json_data)
