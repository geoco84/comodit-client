# control.organizations - Controller for cortex Organizations resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class OrganizationsController(ResourceController):

    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self).__init__()

    def get_collection(self, argv):
        return self._api.organizations()

    def _get_name_argument(self, argv):
        if len(argv) < 1:
            raise ArgumentException("An organization name must be provided");
        return argv[0]

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list                   List all organizations visible to the user
    show <org_name>        Show the details of an organization
    add                    Add an organization
    update <org_name>      Update an organization
    delete <org_name>      Delete an organization
'''
