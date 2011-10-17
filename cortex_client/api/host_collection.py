from directory import Directory
from collection import Collection
from host import Host

class HostCollection(Collection):
    def __init__(self):
        super(HostCollection, self).__init__("hosts")

    def create_host(self, host):
        self.add_resource(host)

    def _new_resource(self, json_data):
        return Host(json_data)

    def get_host(self, uuid):
        return self.get_resource(uuid)

    def get_host_from_path(self, path):
        return self.get_resource_from_path(path)

    def get_uuid(self, path):
        return Directory.get_host_uuid_from_path(path)
