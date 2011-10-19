import os

import cortex_client.util.path as path

from resource import Resource
from cortex_client.util.json_wrapper import StringFactory

class Environment(Resource):
    def __init__(self, api, json_data = None):
        super(Environment, self).__init__(api, api.get_environment_collection(),
                                          json_data)

    def dump(self, output_folder):
        env_folder = os.path.join(output_folder, self.get_name())
        path.ensure(env_folder)
        self.dump_json(os.path.join(env_folder, "definition.json"))

        hosts = self._api.get_host_collection().get_resources({"environmentId" : self.get_uuid()})
        for h in hosts:
            h.dump(env_folder)

    def _show(self, indent = 0):
        print " "*indent, "UUID:", self.get_uuid()
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Organization:", self.get_organization()
        print " "*indent, "Hosts:"
        hosts = self.get_hosts()
        for h in hosts:
            print " "*(indent + 2), h

    def get_organization(self):
        return self._get_field("organization")

    def set_organization(self, value):
        return self._set_field("organization", value)

    def get_hosts(self):
        return self._get_list_field("hosts", StringFactory())

    def set_hosts(self, hosts):
        self._set_list_field("hosts", hosts)

    def get_version(self):
        return self._get_field("version")

    def get_identifier(self):
        org_uuid = self.get_organization()
        org = self._api.get_organization_collection().get_resource(org_uuid)
        return org.get_name() + "/" + self.get_name()
