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
        self._register(["install"], self._install, self._print_install_completions)
        self._register(["uninstall"], self._uninstall, self._print_uninstall_completions)

    def _get_collection(self, org):
        return org.applications()

    def _print_show_file_completions(self, param_num, argv):
        if param_num < 2:
            self._print_resource_completions(param_num, argv)
        elif len(argv) > 1 and param_num == 2:
            org = self._api.organizations().get_resource(argv[0])
            app = org.applications().get_resource(argv[1])
            for f in app.get_files():
                self._print_escaped_name(f.get_name())

    def _show_file(self, argv):
        if len(argv) != 3:
            raise MissingException("Wrong number of arguments")

        app = self._get_resource(argv)
        file_name = argv[2]
        print app.get_file_content(file_name).read()

    def _print_set_file_completions(self, param_num, argv):
        if param_num < 3:
            self._print_show_file_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            self._print_file_completions()

    def _set_file(self, argv):
        if len(argv) != 4:
            raise MissingException("Wrong number of arguments")

        if not os.path.exists(argv[3]):
            raise ArgumentException("Given file does not exist: " + argv[3])

        dist = self._get_resource(argv)
        dist.set_file_content(argv[2], argv[3])

    def _get_environments(self, argv):
        org = self._api.organizations().get_resource(argv[0])
        return org.environments()

    def _get_hosts(self, argv):
        env = self._get_environments(argv).get_resource(argv[1])
        return env.hosts()

    def _get_host(self, argv):
        return self._get_hosts(argv).get_resource(argv[2])

    def _print_hosts_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(self._get_environments(argv))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(self._get_hosts(argv))

    def _print_install_completions(self, param_num, argv):
        if param_num < 3:
            self._print_hosts_completions(param_num, argv)
        elif len(argv) > 1 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            self._print_resource_identifiers(org.applications().get_resources())

    def _install(self, argv):
        if len(argv) != 4:
            raise MissingException("This action takes 4 arguments")

        host = self._get_host(argv)
        app_name = argv[3]
        host.install_application(app_name)

    def _print_uninstall_completions(self, param_num, argv):
        if param_num < 3:
            self._print_hosts_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            host = self._get_host(argv)
            self._print_escaped_names(host.get_applications())

    def _uninstall(self, argv):
        if len(argv) != 4:
            raise MissingException("This action takes 4 arguments")

        host = self._get_host(argv)
        app_name = argv[3]
        host.uninstall_application(app_name)

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>          List all application profiles available to the user
    show <org_name> <app_name>
                             Show the details of an application
    show-file <org_name> <app_name> <name>
                             Show the content of a file resource's template
    set-file <org_name> <app_name> <name> <path>
                             Update the content of a file resource's template
    add   <org_name>         Add an application
    update <org_name> <app_name>
                             Update an application
    delete <org_name> <app_name>
                             Delete an application
    install <org_name> <env_name> <host_name> <app_name>
                            Installs an application on a given host
    uninstall <org_name> <env_name> <host_name> <app_name>
                            Uninstalls an application on a given host
'''
