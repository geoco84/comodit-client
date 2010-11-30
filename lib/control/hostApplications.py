# control.hostApplications - Sub-controller for manageing applications installed on a host.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import json
from control.abstract import AbstractController
from control.exceptions import NotFoundException, MissingException
from rest.client import Client
from util import globals

class HostApplicationsController(AbstractController):

    _resource = "hosts"

    def __init__(self):
        super(HostApplicationsController, self ).__init__()
        self._register(["list"], self._list)
        self._register(["show"], self._show)        
        self._register(["add"], self._add)
        self._register(["update"], self._update)
        self._register(["remove"], self._remove)
        self._default_action = self._list
    
    def _list(self, argv):
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
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid + "/applications")
        
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
    
        if (len(argv) == 0):
            print "You must provide the UUID or name of the application to show."
            exit(-1)
        elif options.uuid:
            application = argv[0]
        else:
            application = self._resolvApplication(argv[0])
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid + "/applications/" + application)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)

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
        result = client.create(self._resource + "/" + item['host'] + "/applications/", item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
            
    def _update(self, argv):
        options = globals.options
                   
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
        elif options.json:
            item = json.loads(options.json)
        else:
            raise MissingException("You must provide a valid object definition with (--json or --file)")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + item['host'] + "/applications/" + item['application'], item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
        
    def _remove(self, argv):
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

    
        if (len(argv) == 0):
            print "You must provide the UUID or name of the application to show."
            exit(-1)
        elif options.uuid:
            application = argv[0]
        else:
            application = self._resolvApplication(argv[0])
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.delete(self._resource + "/" + uuid + "/applications/" + application)
    
    def _render(self, item, detailed=False):
        app = self._getApplicationDetails(item['application'])    
        print app["name"]
        if item.has_key('settings'):
            for setting in item['settings']:
                print "    %-30s: %s" % (setting['key'], setting['value'])

    def _interactive(self, item=None):
        raise NotImplemented
    
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']  
        
    def _resolvApplication(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/application/" + path)
        if result.has_key('uuid') : return result['uuid']
        
    def _getApplicationDetails(self, uuid):            
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("applications/" + uuid)
        return result
        
    def _endpoint(self):
        options = globals.options
        return options.api