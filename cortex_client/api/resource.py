import json

from cortex_client.util.json_wrapper import JsonWrapper
from api_config import ApiConfig

class Resource(JsonWrapper):
    def __init__(self, resource_collection, json_data = None):
        super(Resource, self).__init__(json_data)
        self._resource = resource_collection.get_path()
        self._resource_collection = resource_collection

    def get_uuid(self):
        return self._get_field("uuid")

    def set_uuid(self, uuid):
        self._set_field("uuid", uuid)

    def get_name(self):
        return self._get_field("name")

    def set_name(self, name):
        self._set_field("name", name)

    def get_description(self):
        return self._get_field("description")

    def set_description(self, description):
        self._set_field("description", description)

    def commit(self, force = False):
        parameters = {}
        if(force):
            parameters["force"] = "true"
        self.set_json(ApiConfig.get_client().update(self._resource + "/" +
                                                    self.get_uuid(),
                                                    self.get_json(),
                                                    parameters))

    def create(self):
        self._resource_collection.add_resource(self)

    def delete(self):
        self.set_json(ApiConfig.get_client().delete(self._resource + "/" +
                                                    self._json_data["uuid"]))

    def show(self, as_json = False, indent = 0):
        if(as_json):
            self.print_json()
        else:
            self._show(indent)

    def get_identifier(self):
        return self.get_name()

    def _show(self, indent = 0):
        print " "*indent, "UUID:", self.get_uuid()
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
