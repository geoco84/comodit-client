'''
Created on Nov 22, 2010

@author: eschenal
'''
from util import globals
from control.DefaultController import DefaultController
from rest.Client import Client
from control.Exceptions import NotFoundException, MissingException

class ProvisionerController(DefaultController):

    _resource = "provisioner"

    def __init__(self):
        super(ProvisionerController, self ).__init__()
        self._register(["ks", "kickstart"], self._kickstart)
        self._register(["create"], self._provision)
    
    def _kickstart(self, argv):
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
        result = client.read(self._resource + "/kickstart.cfg", parameters={"hostId":uuid}, decode=False)
        print result.read()
        

    def _provision(self, argv):
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
        result = client.update(self._resource + "/_provision", parameters={"hostId":uuid}, decode=False)
        print result.read()   
        
    def _render(self, item, detailed=False):
        if item.has_key('settings'):
            for setting in item['settings']:
                print "%-30s: %s" % (setting['key'], setting['value'])

    def _interactive(self, item=None):
        raise NotImplemented
    
    def _endpoint(self):
        options = globals.options
        return options.api
    
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']