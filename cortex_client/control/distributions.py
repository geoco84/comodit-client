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

        self._doc = "Distributions handling."

    def _get_collection(self, org):
        return org.distributions()
