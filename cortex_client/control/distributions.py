# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import MissingException, ArgumentException

class DistributionsController(ResourceController):

    _template = "distribution.json"

    def __init__(self):
        super(DistributionsController, self).__init__()
        self._register(["sk", "show-kick"], self._show_kickstart, self._print_show_kick_completions)
        self._register(["set-kick"], self._set_kickstart, self._print_set_kick_completions)

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("Wrong number of arguments");
        return argv[1]

    def get_collection(self, argv):
        if len(argv) == 0:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
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

        if len(argv) != 2:
            raise MissingException("Wrong number of arguments")

        dist.set_kickstart_content(argv[1])

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list            List all distribution profiles available to the user
    show <id>       Show the details of a distribution profile
    show-kick <id>  Show distribution's kickstart template
    set-kick <id> <path>
                    Set distribution's kickstart template's content
    add             Add a distribution profile
    update <id>     Update a distribution profile
    delete <id>     Delete a distribution profile
'''
