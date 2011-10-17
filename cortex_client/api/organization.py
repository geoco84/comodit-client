from resource import Resource
from cortex_client.util.json_wrapper import StringFactory

class Organization(Resource):
    def __init__(self, json_data = None):
        from organization_collection import OrganizationCollection
        super(Organization, self).__init__(OrganizationCollection(), json_data)

    def get_environments(self):
        return self._get_list_field("environments", StringFactory())

    def set_environments(self, environments):
        return self._set_list_field("environments", environments)

    def _show(self, indent = 0):
        print " "*indent, "UUID:", self.get_uuid()
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Environments:", self.get_description()
        environments = self.get_environments()
        for e in environments:
            print " "*(indent + 2), e

    def get_identifier(self):
        return self.get_name()
