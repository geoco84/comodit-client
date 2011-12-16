# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.exceptions import MissingException

class PlatformsController(OrganizationResourceController):

    _template = "platform.json"

    def __init__(self):
        super(PlatformsController, self).__init__()
        self._register(["show-file"], self._show_file, self._print_show_file_completions)
        self._register(["set-file"], self._set_file, self._print_set_file_completions)

    def _get_collection(self, org):
        return org.platforms()

    def _print_show_file_completions(self, param_num, argv):
        if param_num < 2:
            self._print_resource_completions(param_num, argv)
        elif param_num == 2:
            plat = self._get_resource(argv)
            files = plat.get_files()
            for f in files:
                self._print_escaped_name(f.get_name())

    def _show_file(self, argv):

        if len(argv) != 3:
            raise MissingException("Wrong number of arguments")

        plat = self._get_resource(argv)
        print plat.get_file_content(argv[2]).read()

    def _print_set_file_completions(self, param_num, argv):
        if param_num < 3:
            self._print_show_file_completions(param_num, argv)
        elif param_num == 3:
            exit(1)

    def _set_file(self, argv):

        if len(argv) != 4:
            raise MissingException("Wrong number of arguments")

        plat = self._get_resource(argv)
        plat.set_file_content(argv[2], argv[3])

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>                 List all platforms of a given organization
    show <org_name> <plat_name>     Show the details of a platform
    add <org_name>                  Add a platform
    update <org_name> <plat_name>   Update a platform
    delete <org_name> <plat_name>   Delete a platform
'''
