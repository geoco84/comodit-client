# coding: utf-8
from cortex_client.api.collection import Collection
from cortex_client.api.resource import Resource
from cortex_client.control.exceptions import ArgumentException

class ComplianceError(Resource):
    def _get_path(self):
        return self._collection.get_path() + self.get_error_collection() + "/" + self.get_id().replace("/", "%2f")

    def get_error_collection(self):
        return self._get_field("collection")

    def set_error_collection(self, collection):
        return self._set_field("collection", collection)

    def get_id(self):
        return self._get_field("id")

    def set_id(self, new_id):
        return self._set_field("id", new_id)

    def get_name(self):
        return self.get_error_collection() + "/" + self.get_id()

    def _show(self, indent = 0):
        col = self.get_error_collection()
        print "Collection:", col
        print "Id:", self.get_id()

class ComplianceCollection(Collection):
    def _new_resource(self, json_data):
        return ComplianceError(self, json_data)

    def __split_name(self, name):
        slash_index = name.find("/")
        if slash_index == -1:
            raise ArgumentException("Wrong compliance error name, should be of the form <collection>/<id>")
        return (name[0:slash_index], name[slash_index + 1:])

    def get_resource(self, name):
        (col, e_id) = self.__split_name(name)
        error = ComplianceError(self, None)
        error.set_error_collection(col)
        error.set_id(e_id)
        error.update()
        return error
