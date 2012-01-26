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

class OrganizationResourceController(ResourceController):

    def __init__(self):
        super(OrganizationResourceController, self).__init__()

        self._update_action_doc_params("list", "<org_name>")
        self._update_action_doc_params("add", "<org_name>")
        self._update_action_doc_params("delete", "<org_name> <res_name>")
        self._update_action_doc_params("update", "<org_name> <res_name>")
        self._update_action_doc_params("show", "<org_name> <res_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization name must be provided, in addition to resource name");
        return argv[1]

    def _get_collection(self, organization):
        raise NotImplementedError

    def get_collection(self, argv):
        if len(argv) == 0:
            raise ArgumentException("An organization name must be provided");

        org = self._api.organizations().get_resource(argv[0])
        return self._get_collection(org)

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 1:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(self._get_collection(org))

    def _print_list_completions(self, param_num, argv):
        self._print_collection_completions(param_num, argv)

    def _print_show_completions(self, param_num, argv):
        self._print_resource_completions(param_num, argv)

    def _print_add_completions(self, param_num, argv):
        self._print_collection_completions(param_num, argv)

    def _print_update_completions(self, param_num, argv):
        self._print_resource_completions(param_num, argv)

    def _print_delete_completions(self, param_num, argv):
        self._print_resource_completions(param_num, argv)
