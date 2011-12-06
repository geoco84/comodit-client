# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.exceptions import MissingException

class DistributionsController(OrganizationResourceController):

    _template = "distribution.json"

    def __init__(self):
        super(DistributionsController, self).__init__()
        self._register(["sk", "show-kick"], self._show_kickstart, self._print_show_kick_completions)
        self._register(["set-kick"], self._set_kickstart, self._print_set_kick_completions)

    def _get_collection(self, org):
        return org.distributions()

    def _print_distributions(self, argv):
        dists = self._api.get_distribution_collection().get_resources()
        for d in dists:
            self._print_escaped_name(d.get_name())

    def _print_show_kick_completions(self, param_num, argv):
        if param_num == 0:
            self._print_distributions(argv)

    def _show_kickstart(self, argv):
        dist = self._get_resource(argv)
        print dist.get_kickstart_content().read()

    def _print_set_kick_completions(self, param_num, argv):
        if param_num == 0:
            self._print_distributions(argv)
        elif param_num == 1:
            exit(1)

    def _set_kickstart(self, argv):
        dist = self._get_resource(argv)

        if len(argv) != 3:
            raise MissingException("Wrong number of arguments")

        dist.set_kickstart_content(argv[2])

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>
                List all distribution profiles available to the user
    show <org_name> <dist_name>
                Show the details of a distribution
    show-kick <org_name> <dist_name>
                Show distribution's kickstart template
    set-kick <org_name> <dist_name> <path>
                Set distribution's kickstart template's content
    add <org_name>
                Add a distribution profile
    update <org_name> <dist_name>
                Update a distribution profile
    delete <org_name> <dist_name>
                Delete a distribution profile
'''
