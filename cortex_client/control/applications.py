# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.resource import ResourceController
from cortex_client.rest.client import Client
from cortex_client.util import globals


class ApplicationsController(ResourceController):

    _resource = "applications"
    _template = "application.json"

    def __init__(self):
        super(ApplicationsController, self ).__init__()

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else:
            print "Name:", item['name']
            if item.has_key('description'): print "Description:", item['description']
            print "UUID:", item['uuid']
            if item.has_key('packages'):
                print "Packages:"
                for p in item.get('packages'):
                    name = p.get("name")
                    print "   ", name
            if item.has_key('services'):
                print "Services::"
                for p in item.get('services'):
                    name = p.get("name")
                    print "   ", name
            if item.has_key('files'):
                print "Files::"
                for p in item.get('files'):
                    path = p.get("path")
                    print "   ", path


    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/application/" + path)
        if result.has_key('uuid') : return result['uuid']

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list            List all application profiles available to the user
    show [id]       Show the details of an application profile
    add             Add an application profile
    update [id]     Update an application profile
    delete [id]     Delete an application profile
'''
