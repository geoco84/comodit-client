'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.Exceptions import NotFoundException, MissingException
from control.HostApplicationsController import HostApplicationsController
from control.HostDistributionController import HostDistributionController
from control.ResourceController import ResourceController
from util import globals, prompt
from rest.Client import Client

class HostsController(ResourceController):

    _resource = "hosts"

    def __init__(self):
        super(HostsController, self ).__init__()
        self._register(["dist", "distribution"], self._distribution)
        self._register(["app", "application", "applications"], self._applications)
        
    def _list(self, argv):
        options = globals.options
    
        # Validate input parameters
        if options.uuid:
            uuid = options.uuid
        elif options.path:
            uuid = self._resolv(options.path)
            if not uuid: raise NotFoundException(uuid)
        else:
            raise MissingException("You must provide a valid environment UUID (with --uuid) or path (--path)")
        
        self._parameters = {"environmentId":uuid}
        
        super(HostsController, self)._list(argv)           
        
    def _render(self, item, detailed=False):
        print item['uuid'], item['name']
        
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