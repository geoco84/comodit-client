# coding: utf-8

from cortex_client.api import collections

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class GroupsController(ResourceController):

    def __init__(self):
        super(GroupsController, self).__init__()

        # Unregister unsupported actions
        self._unregister(["add", "delete"])

        self._doc = "Groups handling."

    def get_collection(self, argv):
        if len(argv) < 1:
            raise ArgumentException("Wrong number of arguments");

        return collections.groups(self._api, argv[0])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())

    def _print_resource_completions(self, param_num, argv):
        if param_num == 0:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.groups(self._api, argv[0]))

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization name and a group name must be provided")
        return argv[1]
