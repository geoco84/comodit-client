from resource import Resource

class Organization(Resource):
    def __init__(self, json_data = None):
        from organization_collection import OrganizationCollection
        super(Organization, self).__init__(OrganizationCollection(), json_data)

    def _show(self, indent = 0):
        print " "*indent, "UUID:", self._json_data["uuid"]
        print " "*indent, "Name:", self._json_data["name"]
        print " "*indent, "Description:", self._json_data["description"]

    def get_identifier(self):
        return self.get_name()
