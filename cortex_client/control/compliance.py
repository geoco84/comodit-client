# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.api import collections
from cortex_client.control.exceptions import ArgumentException
from cortex_client.control.resource import ResourceController
from cortex_client.control.doc import ActionDoc

class ComplianceController(ResourceController):

    def __init__(self):
        super(ComplianceController, self).__init__()
        self._doc = "Compliance errors handling."

        self._unregister("add")
        self._unregister("update")

        self._register(["delete-all"], self._delete_all, self._print_collection_completions)

        self._register_action_doc(self._delete_all_doc())

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");
        return collections.compliance(self._api, argv[0], argv[1], argv[2])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.environments(self._api, argv[0]))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(collections.hosts(self._api, argv[0], argv[1]))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            errors = collections.compliance(self._api, argv[0], argv[1], argv[2]).get_resources()
            for e in errors:
                self._print_escaped_name(e.get_name())

    def _get_name_argument(self, argv):
        if len(argv) < 4:
            raise ArgumentException("An organization, environment, host and compliance error name must be provided");
        return argv[3]

    def _delete_all(self, argv):
        compliance = self.get_collection(argv)
        compliance.clear_collection()

    def _delete_all_doc(self):
        return ActionDoc("delete-all", "<org_name> <env_name> <host_name>", """
        Deletes all compliance errors.""")
