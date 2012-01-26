# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
#
# Copyright 2011 Guardis SPRL, Liège, Belgium.
# Authors: Gérard Dethier <gerard.dethier@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class RootResourceController(ResourceController):

    def __init__(self):
        super(RootResourceController, self).__init__()

        self._update_action_doc_params("delete", "<res_name>")
        self._update_action_doc_params("update", "<res_name>")
        self._update_action_doc_params("show", "<res_name>")

    def _get_name_argument(self, argv):
        if len(argv) == 0:
            raise ArgumentException("A resource name must be provided");
        return argv[0]

    def _print_resource_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self.get_collection(argv))

    def _print_list_completions(self, param_num, argv):
        pass

    def _print_show_completions(self, param_num, argv):
        self._print_resource_completions(param_num, argv)

    def _print_add_completions(self, param_num, argv):
        pass

    def _print_update_completions(self, param_num, argv):
        self._print_resource_completions(param_num, argv)

    def _print_delete_completions(self, param_num, argv):
        self._print_resource_completions(param_num, argv)
