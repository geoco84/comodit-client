# control.environments - Controller for cortex Environments resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.settings import EnvironmentSettingsController

class EnvironmentsController(OrganizationResourceController):

    _template = "environment.json"

    def __init__(self):
        super(EnvironmentsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], EnvironmentSettingsController())

        self._doc = "Environments handling."

    def _get_collection(self, org):
        return org.environments()
