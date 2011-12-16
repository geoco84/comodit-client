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
        self._register(["show-file"], self._show_file, self._print_show_file_completions)
        self._register(["set-file"], self._set_file, self._print_set_file_completions)

    def _get_collection(self, org):
        return org.distributions()

    def _print_distributions(self, argv):
        dists = self._api.get_distribution_collection().get_resources()
        for d in dists:
            self._print_escaped_name(d.get_name())

    def _print_show_file_completions(self, param_num, argv):
        if param_num < 2:
            self._print_resource_completions(param_num, argv)
        elif param_num == 2:
            dist = self._get_resource(argv)
            files = dist.get_files()
            for f in files:
                self._print_escaped_name(f.get_name())

    def _show_file(self, argv):

        if len(argv) != 3:
            raise MissingException("Wrong number of arguments")

        dist = self._get_resource(argv)
        print dist.get_file_content(argv[2]).read()

    def _print_set_file_completions(self, param_num, argv):
        if param_num < 3:
            self._print_show_file_completions(param_num, argv)
        elif param_num == 3:
            exit(1)

    def _set_file(self, argv):

        if len(argv) != 4:
            raise MissingException("Wrong number of arguments")

        dist = self._get_resource(argv)
        dist.set_file_content(argv[2], argv[3])

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>
                List all distribution profiles available to the user
    show <org_name> <dist_name>
                Show the details of a distribution
    show-file <org_name> <dist_name> <file_name>
                Show a distribution's file template
    set-kick <org_name> <dist_name> <file_name> <path>
                Set a distribution's file template's content
    add <org_name>
                Add a distribution profile
    update <org_name> <dist_name>
                Update a distribution profile
    delete <org_name> <dist_name>
                Delete a distribution profile
'''
