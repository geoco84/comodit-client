# coding: utf-8

from cortex_client.control.root_resource import RootResourceController

class FlavorsController(RootResourceController):

    _template = "user.json"

    def __init__(self):
        super(FlavorsController, self).__init__()

        self._doc = "Flavors handling."

        self._unregister("add")
        self._unregister("update")
        self._unregister("delete")

    def get_collection(self, argv):
        return self._api.flavors()
