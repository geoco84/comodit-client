# control.environments - Controller for cortex Environments resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.organization_resource import OrganizationResourceController

class EnvironmentsController(OrganizationResourceController):

    _template = "environment.json"

    def __init__(self):
        super(EnvironmentsController, self).__init__()

    def _get_collection(self, org):
        return org.environments()

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>         List all environments profiles available to the user
    show <org_name> <app_name>
                            Show the details of an environment
    add   <org_name>        Add an environment
    update <org_name> <app_name>
                            Update an environment
    delete <org_name> <app_name>
                            Delete an environment
'''
