# control.users - Controller for cortex Users resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class UsersController(ResourceController):

    _template = "user.json"

    def __init__(self):
        super(UsersController, self).__init__()

    def get_collection(self, argv):
        return self._api.users()

    def _get_name_argument(self, argv):
        if len(argv) < 1:
            raise ArgumentException("A username must be provided");
        return argv[0]

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list            List all users
    show <username>       Show the details of a user
    add             Add a user
    update <username>     Update a user
    delete <username>     Delete a user
'''
