import json

from api_config import ApiConfig

class Resource(object):
    def __init__(self, resource_collection, json_data = None):
        self._resource = resource_collection.get_path()
        self._resource_collection = resource_collection

        if(json_data):
            self._json_data = json_data
        else:
            self._json_data = {}

    def _get_field(self, field):
        if(self._json_data.has_key(field)):
            return self._json_data[field]
        else:
            return None

    def _set_field(self, field, value):
        self._json_data[field] = value

    def set_json(self, json_data):
        self._json_data = json_data

    def get_json(self):
        return self._json_data

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
        self._json_data = ApiConfig.get_client().update(self._resource + "/" +
                                                        self._json_data["uuid"],
                                                        self._json_data,
                                                        parameters)

    def create(self):
        self._resource_collection.add_resource(self)

    def delete(self):
        self._json_data = ApiConfig.get_client().delete(self._resource + "/" +
                                                        self._json_data["uuid"])

    def show(self, as_json = False, indent = 0):
        if(as_json):
            print json.dumps(self._json_data)
        else:
            self._show(indent)

    def get_identifier(self):
        raise NotImplemented
