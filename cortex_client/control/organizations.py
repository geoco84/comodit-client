# control.organizations - Controller for cortex Organizations resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.root_resource import RootResourceController
from cortex_client.control.exceptions import ArgumentException
from cortex_client.control.settings import OrganizationSettingsController

class OrganizationsController(RootResourceController):

    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], OrganizationSettingsController())

        # actions
        self._register("show-group", self._show_group, self._print_group_completions)
        self._register("add-user", self._add_user, self._print_group_completions)
        self._register("del-user", self._del_user, self._print_group_completions)

    def get_collection(self, argv):
        return self._api.organizations()

    def _print_group_completions(self, param_num, argv):
        if param_num < 1:
            self._print_resource_completions(param_num, argv)
        elif param_num == 1:
            org = self._get_resource(argv)
            self._print_identifiers(org.groups())

    def _show_group(self, argv):
        if len(argv) != 2:
            raise ArgumentException("This action takes 2 arguments")

        org = self._get_resource(argv)

        group = org.groups().get_resource(argv[1])
        group.show()

    def _add_user(self, argv):
        if len(argv) != 3:
            raise ArgumentException("This action takes 3 arguments")

        org = self._get_resource(argv)

        group = org.groups().get_resource(argv[1])
        group.add_user(argv[2])
        group.commit()

    def _del_user(self, argv):
        if len(argv) != 3:
            raise ArgumentException("This action takes 3 arguments")

        org = self._get_resource(argv)

        group = org.groups().get_resource(argv[1])
        group.remove_user(argv[2])
        group.commit()

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list                   List all organizations visible to the user
    show <org_name>        Show the details of an organization
    show-group <org_name> <group_name>
                           Show a group of an organization
    add                    Add an organization
    add-user <org_name> <group_name> <user_name>
                           Add a user to a group
    update <org_name>      Update an organization
    delete <org_name>      Delete an organization
'''
