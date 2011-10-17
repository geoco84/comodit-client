from collection import Collection
from directory import Directory
from organization import Organization

class OrganizationCollection(Collection):
    def __init__(self):
        super(OrganizationCollection, self).__init__("organizations")

    def _new_resource(self, json_data):
        return Organization(json_data)

    def get_uuid(self, path):
        return Directory.get_organization_uuid(path)
