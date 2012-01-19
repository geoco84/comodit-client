# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.settings import DistributionSettingsController
from cortex_client.control.files import DistributionFilesController
from cortex_client.control.parameters import DistributionParametersController

class DistributionsController(OrganizationResourceController):

    _template = "distribution.json"

    def __init__(self):
        super(DistributionsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], DistributionSettingsController())
        self._register_subcontroller(["files"], DistributionFilesController())
        self._register_subcontroller(["parameters"], DistributionParametersController())

    def _get_collection(self, org):
        return org.distributions()

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>
                List all distribution profiles available to the user
    show <org_name> <dist_name>
                Show the details of a distribution
    show-file <org_name> <dist_name> <file_name>
                Show a distribution's file template
    set-file <org_name> <dist_name> <file_name> <path>
                Set a distribution's file template's content
    add <org_name>
                Add a distribution profile
    update <org_name> <dist_name>
                Update a distribution profile
    delete <org_name> <dist_name>
                Delete a distribution profile
    settings <...>
                Settings handling
    files <...> Files handling
'''
