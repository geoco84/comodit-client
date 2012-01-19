# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.files import ApplicationFilesController
from cortex_client.control.parameters import ApplicationParametersController

class ApplicationsController(OrganizationResourceController):

    _template = "application.json"

    def __init__(self):
        super(ApplicationsController, self).__init__()

        # sub-controllers
        self._register_subcontroller(["files"], ApplicationFilesController())
        self._register_subcontroller(["parameters"], ApplicationParametersController())

    def _get_collection(self, org):
        return org.applications()

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>          List all application profiles available to the user
    show <org_name> <app_name>
                             Show the details of an application
    add   <org_name>         Add an application
    update <org_name> <app_name>
                             Update an application
    delete <org_name> <app_name>
                             Delete an application
    files <...>
                             File resources handling
    parameters <...>
                             Parameters handling
'''
