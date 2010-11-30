# control.hosts - Controller for cortex Hosts resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

from util import globals
from control.resource import ResourceController
from control.exceptions import NotFoundException, MissingException
from rest.client import Client
from control.hostDistribution import HostDistributionController
from control.hostApplications import HostApplicationsController

class HostsController(ResourceController):

    _resource = "hosts"
    _template = "host.json"    

    def __init__(self):
        super(HostsController, self ).__init__()
        self._register(["dist", "distribution"], self._distribution)
        self._register(["app", "application", "applications"], self._applications)
        
    def _list(self, argv):
        options = globals.options
    
        # Validate input parameters
        if options.env_uuid:
            uuid = options.env_uuid
        elif options.env_path:
            path = options.env_path
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        elif options.env and options.uuid:
            uuid = options.env
        elif options.env:
            path = options.env
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        else:
            raise MissingException("You must provide a valid environment UUID (with --env-uuid) or path (--env-path)")
        
        self._parameters = {"environmentId":uuid}
        
        super(HostsController, self)._list(argv)           
        
    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else:
            print "Name:", item['name']
            print "UUUID:", item['uuid']
            if item.has_key('description'):
                print "Description:", item['description']
        
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']        

    def _distribution(self, argv):
        controller = HostDistributionController()
        controller.run(argv)
        
    def _applications(self, argv):
        controller = HostApplicationsController()
        controller.run(argv)        