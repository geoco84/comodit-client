# control.environments - Controller for cortex Environments resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.util import globals
from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import NotFoundException, MissingException
from cortex_client.rest.client import Client

class EnvironmentsController(ResourceController):

    _resource = "environments"
    _template = "environment.json"

    def __init__(self):
        super(EnvironmentsController, self ).__init__()

    def _list(self, argv):
        options = globals.options

        # Validate input parameters
        if options.org_uuid:
            uuid = options.org_uuid
        elif options.org_path:
            path = options.org_path
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        elif options.org and options.uuid:
            uuid = options.org
        elif options.org:
            path = options.org
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        else:
            uuid = None

        if uuid: self._parameters = {"organizationId":uuid}

        super(EnvironmentsController, self)._list(argv)

    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else:
            print "Name:", item['name']
            print "UUUID:", item['uuid']
            if item.has_key('description'):
                print "Description:", item['description']
            if item.has_key('settings'):
                print "Settings:"
                for setting in item['settings']:
                    print "    %-30s: %s" % (setting['key'], setting['value'])

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list --org [id]    List all environments within an organization
    show [id]          Show the details of an environment
    add                Add an environment
    update [id]        Update an environment
    delete [id]        Delete an environment
'''
