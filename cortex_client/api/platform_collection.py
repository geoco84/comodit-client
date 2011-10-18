from collection import Collection
from directory import Directory
from platform import Platform

class PlatformCollection(Collection):
    def __init__(self):
        super(PlatformCollection, self).__init__("platforms")

    def _new_resource(self, json_data):
        return Platform(json_data)

    def get_uuid(self, path):
        return Directory.get_platform_uuid(path)
