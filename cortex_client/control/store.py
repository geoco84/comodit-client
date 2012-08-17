from cortex_client.control.root_resource import RootResourceController

class AppStoreController(RootResourceController):

    def __init__(self):
        super(AppStoreController, self).__init__()

        self._unregister("add")
        self._unregister("update")
        self._unregister("delete")

        self._doc = "Application store handling."

    def get_collection(self, argv):
        return self._api.app_store()

class DistStoreController(RootResourceController):

    def __init__(self):
        super(DistStoreController, self).__init__()

        self._unregister("add")
        self._unregister("update")
        self._unregister("delete")

        self._doc = "Distribution store handling."

    def get_collection(self, argv):
        return self._api.dist_store()
