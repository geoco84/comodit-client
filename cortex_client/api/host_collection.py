from directory import Directory
from collection import Collection
from host import Host

class HostCollection(Collection):
    def __init__(self):
        super(HostCollection, self).__init__("hosts")

    def _new_resource(self, json_data):
        return Host(json_data)

    def get_uuid(self, path):
        return Directory.get_host_uuid_from_path(path)
