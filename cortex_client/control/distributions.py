# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.api.distribution_collection import DistributionCollection

class DistributionsController(ResourceController):

    _template = "distribution.json"

    def __init__(self):
        super(DistributionsController, self ).__init__()
        self._collection = DistributionCollection()

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list            List all distribution profiles available to the user
    show [id]       Show the details of a distribution profile
    add             Add a distribution profile
    update [id]     Update a distribution profile
    delete [id]     Delete a distribution profile
'''
