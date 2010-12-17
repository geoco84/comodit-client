# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

from control.resource import ResourceController
from rest.client import Client
from util import globals

class DistributionsController(ResourceController):

    _resource = "distributions"
    _template = "distribution.json"

    def __init__(self):
        super(DistributionsController, self ).__init__()

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else: 
            print "Name:", item['name']
            if item.has_key('description'): print "Description:", item['description']
            print "UUID:", item['uuid']
            if item.has_key('url'): print "Url:", item['url']
            if item.has_key('initrd'): print "Initrd:", item['initrd']
            if item.has_key('vmlinuz'): print "Vmlinuz:", item['vmlinuz']

    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/distribution/" + path)
        if result.has_key('uuid') : return result['uuid']            

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource. 
        
Actions:
    list            List all distribution profiles available to the user
    show [id]       Show the details of a distribution profile
    add             Add a distribution profile
    update [id]     Update a distribution profile
    delete [id]     Delete a distribution profile
'''