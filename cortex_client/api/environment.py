from resource import Resource
from organization_collection import OrganizationCollection

class Environment(Resource):
    def __init__(self, json_data = None):
        from environment_collection import EnvironmentCollection
        super(Environment, self).__init__(EnvironmentCollection(), json_data)
        self._org_collection = OrganizationCollection()

    def _show(self, indent = 0):
        print " "*indent, "UUID:", self.get_uuid()
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Organization:", self.get_organization()

    def get_organization(self):
        return self._get_field("organization")

    def set_organization(self, value):
        return self._set_field("organization", value)

    def get_identifier(self):
        org_uuid = self.get_organization()
        org = self._org_collection.get_resource(org_uuid)
        return org.get_name() + "/" + self.get_name()
