# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import os

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.exceptions import MissingException, ArgumentException

class ApplicationsController(OrganizationResourceController):

    _template = "application.json"

    def __init__(self):
        super(ApplicationsController, self).__init__()
        self._register(["show-file"], self._show_file, self._print_show_file_completions)
        self._register(["set-file"], self._set_file, self._print_set_file_completions)

    def _get_collection(self, org):
        return org.applications()

    def _print_applications(self, argv):
        apps = self._api.get_application_collection().get_resources()
        for a in apps:
            self._print_escaped_name(a.get_name())

    def _print_files(self, argv):
        if(len(argv) > 0):
            app = self._get_application(argv[0])
            for f in app.get_files():
                self._print_escaped_name(f.get_name())

    def _print_show_file_completions(self, param_num, argv):
        if param_num == 0:
            self._print_applications(argv)
        elif param_num == 1:
            self._print_files(argv)

    def _show_file(self, argv):
        if len(argv) != 3:
            raise MissingException("Wrong number of arguments")

        app = self._get_resource(argv)
        file_name = argv[2]
        print app.get_file_content(file_name).read()

    def _print_set_file_completions(self, param_num, argv):
        if param_num == 0:
            self._print_applications(argv)
        elif param_num == 1:
            self._print_files(argv)
        elif param_num == 2:
            exit(1)

    def _set_file(self, argv):
        if len(argv) != 4:
            raise MissingException("Wrong number of arguments")

        if not os.path.exists(argv[3]):
            raise ArgumentException("Given file does not exist: " + argv[3])

        dist = self._get_resource(argv)
        dist.set_file_content(argv[2], argv[3])

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>          List all application profiles available to the user
    show <org_name> <app_name>
                             Show the details of an application profile
    show-file <org_name> <app_name> <name>
                             Show the content of a file resource's template
    set-file <org_name> <app_name> <name> <path>
                             Update the content of a file resource's template
    add   <org_name>         Add an application profile
    update <org_name> <app_name>
                             Update an application profile
    delete <org_name> <app_name>
                             Delete an application profile
'''
