# control.hosts - Controller for cortex Hosts resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import json

from cortex_client.util import globals
from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import NotFoundException, MissingException
from cortex_client.rest.client import Client

class HostsController(ResourceController):

    _resource = "hosts"
    _template = "host.json"

    def __init__(self):
        super(HostsController, self ).__init__()
        self._register(["s", "state"], self._state)

    def _list(self, argv):
        options = globals.options
        self._parameters = {}

        # Validate input parameters
        if options.env_uuid:
            uuid = options.env_uuid
        elif options.env_path:
            path = options.env_path
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        elif options.env and options.uuid:
            uuid = options.env
        elif options.env:
            path = options.env
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        else :
            uuid = None

        if uuid : self._parameters["environmentId"] = uuid

        super(HostsController, self)._list(argv)

    def _state(self, argv):
        options = globals.options

        # Require an object as argument
        if len(argv) == 0:
            raise MissingException("You must provide a valid object identifier")

        # Validate input parameters
        uuid = argv[0]

        # Query the server
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid + "/state")

        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._renderState(result)

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else:
            print "Name:", item['name']
            print "UUUID:", item['uuid']
            if item.has_key('description'):
                print "Description:", item['description']

    def _renderState(self, item,):
        print "State:", item['state']
        if item.has_key('cpuTime'):
            print "CPU Time:", item['cpuTime']

    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']


    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list --env [id]    List all hosts within an environment
    show [id]          Show the details of a host
    state [id]         Show the state of a host
    add                Add an host
    update [id]        Update a host
    delete [id]        Delete a host

'''
