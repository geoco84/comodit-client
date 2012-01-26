# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.settings import PlatformSettingsController
from cortex_client.control.files import PlatformFilesController
from cortex_client.control.parameters import PlatformParametersController

class PlatformsController(OrganizationResourceController):

    _template = "platform.json"

    def __init__(self):
        super(PlatformsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], PlatformSettingsController())
        self._register_subcontroller(["files"], PlatformFilesController())
        self._register_subcontroller(["parameters"], PlatformParametersController())

        self._doc = "Platforms handling."

    def _get_collection(self, org):
        return org.platforms()
