from api_config import ApiConfig
from host import Host
from directory import Directory
from collection import Collection

class HostCollection(Collection):
    def __init__(self):
        super(HostCollection, self).__init__("hosts")

    @classmethod
    def get_hosts(self, env_uuid = None, env_path = None):
        parameters = {}
        if(env_uuid != None):
            parameters["environmentId"] = env_uuid
        elif(env_path != None):
            parameters["environmentId"] = Directory.get_environment_uuid_from_path(self, env_path)

        result = ApiConfig.get_client().read("hosts",
                                  parameters = parameters)

        hosts_list = []
        if(result["count"] != "0"):
            json_list = result["items"]
            for json_host in json_list:
                hosts_list.append(Host(json_data = json_host))

        return hosts_list

    @classmethod
    def create_host(self, host):
        self.add_resource(host)

    @classmethod
    def get_host(self, uuid):
        result = ApiConfig.get_client().read("hosts/"+uuid)
        return Host(result)

    @classmethod
    def get_host_from_path(self, path):
        uuid = Directory.get_host_uuid_from_path(path)
        result = ApiConfig.get_client().read("hosts/"+uuid)
        return Host(result)
