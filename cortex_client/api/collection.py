class Collection(object):
    def __init__(self, resource_path, api):
        self._resource_path = resource_path
        self._api = api

    def get_path(self):
        return self._resource_path

    def add_resource(self, resource):
        result = self._client.create(self._resource_path,
                                               resource.get_json())
        resource.set_json(result)

    def get_resources(self, parameters = {}):
        client = self._api.get_client()
        result = client.read(self._resource_path, parameters)

        resources_list = []
        if(result["count"] != "0"):
            json_list = result["items"]
            for json_res in json_list:
                resources_list.append(self._new_resource(json_res))

        return resources_list

    def _new_resource(self, json_data):
        raise NotImplementedError

    def get_resource(self, uuid):
        client = self._api.get_client()
        result = client.read(self._resource_path + "/" + uuid)
        return self._new_resource(result)

    def get_resource_from_path(self, path):
        return self.get_resource(self.get_uuid(path))

    def get_uuid(self, path):
        raise NotImplementedError
