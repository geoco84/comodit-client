# control.organizations - Controller for cortex Organizations resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.util import globals
from cortex_client.control.resource import ResourceController
from cortex_client.rest.client import Client

class OrganizationsController(ResourceController):

    _resource = "organizations"
    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self ).__init__()

    def _render(self, item, detailed=False):
        print item['uuid'], item['name']

        if detailed:
            if item.has_key('description'):
                print "   ", item['description']


    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list            List all organizations visible to the user
    show [id]       Show the details of an organization
    add             Add an organization
    update [id]     Update an organization
    delete [id]     Delete an organization
'''
