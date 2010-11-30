# control.hostDistributions - Sub-controller for managing the distribution installed on a host.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import json, os

from util import globals
from control.abstract import AbstractController
from control.exceptions import NotFoundException, MissingException
from rest.client import Client
from util.editor import edit_text

TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates'))

class HostDistributionController(AbstractController):

    _resource = "hosts"
    _template = "distribution-settings.json"
    
    def __init__(self):
        super(HostDistributionController, self ).__init__()
        self._register(["show"], self._show)
        self._register(["set"], self._set)
        self._default_action = self._show
    
    def _show(self, argv):
        options = globals.options
    
        uuid= self._param_host()
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid+ "/distribution")
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result, detailed=True)
            
    def _set(self, argv):
        options = globals.options
        
        client = Client(self._endpoint(), options.username, options.password)
        
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
                host = item['host']
        elif options.json:
            item = json.loads(options.json)
            host = item['host']
        else:
            host = self._param_host()
            try:
                item = client.read(self._resource + "/" + host + "/distribution")
                original = json.dumps(item, sort_keys=True, indent=4)
            except:
                original = open(os.path.join(TEMPLATE_DIR, self._template)).read()
            updated = edit_text(original)
            item = json.loads(updated)   

        result = client.update(self._resource + "/" + host + "/distribution", item)
        
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
    
    def _param_host(self):
        options = globals.options
                
        # Validate input parameters
        if options.host_uuid:
            uuid = options.host_uuid
        elif options.host_path:
            path = options.host_path
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        elif options.host and options.uuid:
            uuid = options.host
        elif options.host:
            path = options.host
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        else:
            raise MissingException("You must provide a valid host UUID (with --host-uuid) or path (--host-path)")
        return uuid    