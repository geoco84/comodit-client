class Client(object):
    def __init__(self, endpoint, username, password):
        pass

class CortexApi(object):
    def __init__(self, endpoint, username, password):
        self._client = Client(endpoint, username, password)

    def get_client(self):
        return self._client
