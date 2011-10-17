from api_config import ApiConfig
from collection import Collection
from directory import Directory
from organization import Organization

class OrganizationCollection(Collection):
    def __init__(self):
        super(OrganizationCollection, self).__init__("organizations")

    def _new_resource(self, json_data):
        return Organization(json_data)

    def create_organization(self, host):
        self.add_resource(host)

    def get_organizations(self):
        return self.get_resources()

    def get_organization(self, uuid):
        result = ApiConfig.get_client().read("organizations/"+uuid)
        return Organization(result)

    def get_organization_from_path(self, path):
        uuid = Directory.get_organization_uuid(path)
        return self.get_organization(uuid)

    def get_uuid(self, path):
        return Directory.get_organization_uuid(path)