# coding: utf-8
from cortex_client.util.json_wrapper import JsonWrapper
from cortex_client.api.collection import Collection

class Log(JsonWrapper):
    def get_timestamp(self):
        return self._get_field("timestamp")

    def get_message(self):
        return self._get_field("message")

class AuditCollection(Collection):
    def _new_resource(self, json_data):
        return Log(json_data)
