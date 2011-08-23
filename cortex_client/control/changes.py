# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.exceptions import MissingException, NotFoundException
from cortex_client.control.resource import ResourceController
from cortex_client.rest.client import Client
from cortex_client.util import globals, prompt


class ChangesController(ResourceController):

    _resource = "changes"
    _template = "change.json"

    def __init__(self):
        super(ChangesController, self ).__init__()

    def _delete(self, argv):
        options = globals.options

        # Require an object as argument
        if len(argv) == 0:
            raise MissingException("You must provide a valid object identifier")

        # Validate input parameters
        if options.uuid:
            uuid = argv[0]
        else:
            uuid = self._resolv(argv[0])
            if not uuid: raise NotFoundException(uuid)

        client = Client(self._endpoint(), options.username, options.password)
        item = client.read(self._resource + "/" + uuid)

        if (prompt.confirm(prompt="Delete change made at " + item['timestamp'] + " ?", resp=False)) :
            client.delete(self._resource + "/" + uuid)

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['action']
        else:
            print "UUID:", item['uuid']
            print "Action:", item['action']
            print "Timestamp", item['timestamp']

    def _resolv(self, path):
        pass

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list            List all parameters available to the user
    show [id]       Show the details of a parameter
    add             Add a parameter profile
    update [id]     Update a parameter profile
    delete [id]     Delete a parameter profile
'''
