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
from cortex_client.control.groups import GroupsController

class OrganizationsController(RootResourceController):

    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], OrganizationSettingsController())
        self._register_subcontroller(["groups"], GroupsController())

        self._doc = "Organizations handling."

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
