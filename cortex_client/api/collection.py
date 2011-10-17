from api_config import ApiConfig

class Collection(object):
    def __init__(self, resource_path):
        self._resource_path = resource_path

    def get_path(self):
        return self._resource_path

    def add_resource(self, resource):
        result = ApiConfig.get_client().create(self._resource_path,
                                               resource.get_json())
        resource.set_json(result)

    def remove_resource(self, resource):
        result = ApiConfig.get_client().delete(self._resource_path,
                                               resource.get_json())
        resource.set_json(result)
