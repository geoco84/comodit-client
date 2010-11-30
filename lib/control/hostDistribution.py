# control.hostDistributions - Sub-controller for managing the distribution installed on a host.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import json

from util import globals
from control.abstract import AbstractController
from control.exceptions import NotFoundException, MissingException
from rest.client import Client

class HostDistributionController(AbstractController):

    _resource = "hosts"

    def __init__(self):
        super(HostDistributionController, self ).__init__()
        self._register(["show"], self._show)
        self._register(["set"], self._set)
        self._default_action = self._show
    
    def _show(self, argv):
        options = globals.options
    
        # Validate input parameters
        if options.uuid:
            uuid = options.uuid
        elif options.path:
            uuid = self._resolv(options.path)
            if not uuid: raise NotFoundException(uuid)
        else:
            raise MissingException("You must provide a valid host UUID (with --uuid) or path (--path)")
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid+ "/distribution")
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result, detailed=True)
            
    def _set(self, argv):
        options = globals.options
          
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
        elif options.json:
            item = json.loads(options.json)
        else:
            raise MissingException("You must provide a valid object definition with (--json or --file)")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + item['host'] + "/distribution", item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
        
    def _render(self, item, detailed=False):
        dist = self._getDistributionDetails(item['distribution'])    
        print dist["name"]
        if item.has_key('settings'):
            for setting in item['settings']:
                print "    %-30s: %s" % (setting['key'], setting['value'])
    
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']   

    def _getDistributionDetails(self, uuid):            
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("distributions/" + uuid)
        return result        
    
    def _endpoint(self):
        options = globals.options
        return options.api