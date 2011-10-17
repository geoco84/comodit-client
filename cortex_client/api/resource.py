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
        self._resource_collection.remove_resource(self)

    def show(self, as_json = False, ident = 0):
        raise NotImplemented

    def get_identifier(self):
        raise NotImplemented
