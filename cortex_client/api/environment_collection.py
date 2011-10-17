from collection import Collection
from directory import Directory
from environment import Environment

class EnvironmentCollection(Collection):
    def __init__(self):
        super(EnvironmentCollection, self).__init__("environments")

    def _new_resource(self, json_data):
        return Environment(json_data)

    def get_uuid(self, path):
        return Directory.get_environment_uuid_from_path(path)
