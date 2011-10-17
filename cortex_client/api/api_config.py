from cortex_client.rest.client import Client

class ApiConfig(object):
    _client = None

    @classmethod
    def init(cls, endpoint, username, password):
        cls._client = Client(endpoint, username, password)

    @classmethod
    def get_client(cls):
        return cls._client
