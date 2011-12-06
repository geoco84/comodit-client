# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
#
# Copyright 2011 Guardis SPRL, Liège, Belgium.
# Authors: Gérard Dethier <gerard.dethier@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class OrganizationResourceController(ResourceController):

    def __init__(self):
        super(OrganizationResourceController, self).__init__()

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization name must be provided, in addition to resource name");
        return argv[1]

    def _get_collection(self, organization):
        raise NotImplementedError

    def get_collection(self, argv):
        if len(argv) == 0:
            raise ArgumentException("An organization name must be provided");

        org = self._api.organizations().get_resource(argv[0])
        return self._get_collection(org)
