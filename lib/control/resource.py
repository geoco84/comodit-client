# control.resource - Generic controller for managing cortex resources. 
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import json

from control.abstract import AbstractController
from util import globals, prompt
from rest.client import Client
from control.exceptions import NotFoundException, MissingException


class ResourceController(AbstractController):

    _resource = ""
    _parameters = {}

    def __init__(self):
        super(ResourceController, self).__init__()
        self._register(["l", "list"], self._list)
        self._register(["s", "show"], self._show)
        self._register(["a", "add"], self._add)
        self._register(["u", "update"], self._update)        
        self._register(["d", "delete"], self._delete)
        self._default_action = self._list
        
    def _list(self, argv):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource, parameters=self._parameters)
    
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else: 
            if (result['count'] == "0"):
                print "Request returned 0 object."
            else:
                for o in result['items']:
                    self._render(o)
    
    def _show(self, argv):
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
            
        # Query the server
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid)
        
        # Display the result
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result, detailed=True)
    
    def _add(self, argv):
        options = globals.options
       
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
        elif options.json:
            item = json.loads(options.json)            
        else:
            raise MissingException("You must provide a valid object definition with (--json or --file)")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.create(self._resource, item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
    
    def _update(self, argv):
        options = globals.options
          
        client = Client(self._endpoint(), options.username, options.password)
        
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
                uuid = item.get("uuid")
        elif options.json:
            item = json.loads(options.json)
            uuid = item.get("uuid")
            raise MissingException("You must provide a valid object definition with (--json or --file)")
            
            item = client.read(self._resource + "/" + uuid)
            item = self._interactive(item)
        else:
            raise MissingException("You must provide a valid object definition with (--json or --file)")            
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + uuid, item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
    
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
        
        if (prompt.confirm(prompt="Delete " + item['name'] + " ?", resp=False)) :
            client.delete(self._resource + "/" + uuid)
    
    def _render(self, item, detailed=False):
        pass

    def _resolv(self, path):
        pass
                        
    def _endpoint(self):
        options = globals.options
        return options.api
