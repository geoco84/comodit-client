# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class PlatformsController(ResourceController):

    _template = "platform.json"

    def __init__(self):
        super(PlatformsController, self).__init__()

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("Wrong number of arguments");
        return argv[1]

    def get_collection(self, argv):
        if len(argv) == 0:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        return org.platforms()

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>                 List all platforms of a given organization
    show <org_name> <plat_name>     Show the details of a platform
    add                             Add a platform
    update <id>                     Update a platform
    delete <id>                     Delete a platform
'''
