# control.organizations - Controller for cortex Organizations resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.api.organization_collection import OrganizationCollection
from cortex_client.api.organization import Organization

class OrganizationsController(ResourceController):

    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self ).__init__()
        self._collection = OrganizationCollection()

    def _new_resource(self, json_data):
        return Organization(json_data)

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list            List all organizations visible to the user
    show [id]       Show the details of an organization
    add             Add an organization
    update [id]     Update an organization
    delete [id]     Delete an organization
'''
