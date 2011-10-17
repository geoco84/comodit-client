import json

from api_config import ApiConfig
from cortex_client.api.resource import Resource
from cortex_client.rest.exceptions import ApiException
from environment_collection import EnvironmentCollection

class Setting(object):
    def __init__(self, json_data = None):
        if(json_data):
            self._json_data = json_data
        else:
            self._json_data = {}

    @classmethod
    def show_json(cls, json_data, indent = 0):
        print " "*indent, "Value:", json_data["value"]
        print " "*indent, "Key:", json_data["key"]
        print " "*indent, "Version:", json_data["version"]

    def show(self, as_json = False, indent = 0):
        if(as_json):
            print json.dumps(self._json_data, indent = 4)
        else:
            self.show_json(self._json_data, indent)

class HostInfo(object):
    def __init__(self, json_data = None):
        if(json_data):
            self._json_data = json_data
        else:
            self._json_data = {}

    def get_state(self):
        return self._json_data["state"]

    def show(self, indent = 0, as_json = False):
        if(as_json):
            print json.dumps(self._json_data, indent = 4)
        else:
            print " "*indent, self._json_data["state"]

class Host(Resource):
    def __init__(self, json_data = None):
        from cortex_client.api.host_collection import HostCollection
        super(Host, self).__init__(HostCollection(), json_data)
        self._env_collection = EnvironmentCollection()

    def get_organization(self):
        return self._get_field("organization")

    def set_organization(self, organization):
        self._set_field("organization", organization)

    def get_environment(self):
        return self._get_field("environment")

    def set_environment(self, environment):
        self._set_field("environment", environment)

    def get_platform(self):
        return self._get_field("platform")

    def set_platform(self, platform):
        self._set_field("platform", platform)

    def get_distribution(self):
        return self._get_field("distribution")

    def set_distribution(self, distribution):
        self._set_field("distribution", distribution)

    def get_settings(self):
        settings = []
        json_settings = self._get_field("settings")
        if(json_settings):
            for s in json_settings:
                settings.append(Setting(s))
        return settings

    def set_settings(self, settings):
        json_settings = []
        for s in settings:
            json_settings.append(s.get_json())
        self._set_field("settings", json_settings)

    def delete(self, delete_vm = False):
        if(delete_vm):
            try:
                ApiConfig.get_client().update("hosts/" + self.get_uuid() + "/_delete",
                                              decode=False)
            except ApiException, e:
                if(e.code == 400):
                    print "Could not delete VM:", e.message
                else:
                    raise e
        ApiConfig.get_client().delete("hosts/" + self.get_uuid())

    def get_state(self):
        result = ApiConfig.get_client().read("hosts/" + self.get_uuid()+"/state")
        return HostInfo(result)

    def get_identifier(self):
        env_uuid = self.get_environment()
        env = self._env_collection.get_resource(env_uuid)
        return env.get_identifier() + "/" + self.get_name()

    def _show(self, as_json = False, indent = 0):
        print " "*indent, "UUID:", self.get_uuid()
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Organization:", self.get_organization()
        print " "*indent, "Environment:", self.get_environment()
        print " "*indent, "Platform:", self.get_platform()
        print " "*indent, "Distribution:", self.get_distribution()
        print " "*indent, "Settings:"
        settings = self.get_settings()
        if(settings):
            for s in self.get_settings():
                s.show(indent=(indent + 2))
                print
        else:
            print " "*(indent + 2), "None"

    def start(self):
        result = ApiConfig.get_client().update("hosts/"+self.get_uuid()+"/_start", decode=False)
        if(result.getcode() != 202):
            raise "Call not accepted by server"

    def pause(self):
        result = ApiConfig.get_client().update("hosts/"+self.get_uuid()+"/_pause", decode=False)
        if(result.getcode() != 202):
            raise "Call not accepted by server"

    def resume(self):
        result = ApiConfig.get_client().update("hosts/"+self.get_uuid()+"/_resume", decode=False)
        if(result.getcode() != 202):
            raise "Call not accepted by server"

    def shutdown(self):
        result = ApiConfig.get_client().update("hosts/"+self.get_uuid()+"/_stop", decode=False)
        if(result.getcode() != 202):
            raise "Call not accepted by server"

    def poweroff(self):
        result = ApiConfig.get_client().update("hosts/"+self.get_uuid()+"/_off", decode=False)
        if(result.getcode() != 202):
            raise "Call not accepted by server"
