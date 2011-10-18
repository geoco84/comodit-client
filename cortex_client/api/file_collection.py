from collection import Collection
from directory import Directory
from file import File
from api_config import ApiConfig

class FileCollection(Collection):
    def __init__(self):
        super(FileCollection, self).__init__("files")

    def _new_resource(self, json_data):
        return File(json_data)

    def get_uuid(self, path):
        raise NotImplementedError

    def get_resource(self, uuid):
        result = ApiConfig.get_client().read(self._resource_path + "/"+uuid + "/_meta")
        return self._new_resource(result)