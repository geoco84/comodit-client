# control.users - Controller for cortex Users resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import sys, json

from util import globals
from control.resource import ResourceController
from control.exceptions import ControllerException
from rest.client import Client

class UsersController(ResourceController):

    _resource = "users"

    def __init__(self):
        super(UsersController, self ).__init__()
        
    def _update(self, args):
        options = globals.options
                  
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
                uuid = item.get("uuid")
        elif options.json:
            item = json.loads(options.json)
            uuid = item.get("uuid")
        else:
            raise ControllerException("Updating a user is not possible in interactive mode.")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + uuid, item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['username']
        else: 
            print "Username:", item['username']
            print "UUID:", item['uuid']
            sys.stdout.write("Roles: ")
            map(lambda x: sys.stdout.write(x+ " "), item['roles'])
            sys.stdout.write("\r\n")


    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/user/" + path)
        if result.has_key('uuid') : return result['uuid']            