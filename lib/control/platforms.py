# control.applications - Controller for cortex Applications resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

from control.exceptions import ControllerException
from control.resource import ResourceController
from rest.client import Client
from util import globals
import json


class PlatformsController(ResourceController):

    _resource = "platforms"
    _template = "platform.json"

    def __init__(self):
        super(PlatformsController, self ).__init__()

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else: 
            print "Name:", item['name']
            print "UUID:", item['uuid']
            if item.has_key('description'): print "Description:", item['description']
            if item.has_key('driver'): print "Driver:", item['driver']


    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/platform/" + path)
        if result.has_key('uuid') : return result['uuid']
    
    def _help(self, argv):
        print '''You must provide an action to perfom on this resource. 
        
Actions:
    list            List all platforms available to the user
    show [id]       Show the details of a platform
    add             Add a platform
    update [id]     Update a platform
    delete [id]     Delete a platform
'''