# control.organizations - Controller for cortex Organizations resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

from util import globals
from control.resource import ResourceController
from rest.client import Client

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