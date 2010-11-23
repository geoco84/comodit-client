'''
Created on Nov 22, 2010

@author: eschenal
'''
from util import globals
from control.DefaultController import DefaultController, ControllerException
from rest.Client import Client
import json
from control.Exceptions import NotFoundException, MissingException

class HostDistributionController(DefaultController):

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
            raise MissingException("You must provide a valid environment UUID (with --uuid) or path (--path)")
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid+ "/distribution")
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result, detailed=True)
            
    def _set(self, argv):
        options = globals.options
          
        # Validate input parameters
        if options.uuid:
            uuid = options.uuid
        elif options.path:
            uuid = self._resolv(options.path)
            if not uuid: raise NotFoundException(uuid)
        else:
            raise MissingException("You must provide a valid environment UUID (with --uuid) or path (--path)")
          
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
        elif options.json:
            item = json.loads(options.json)
        else:
            raise ControllerException("Setting a distribution is not possible in interactive mode.")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + uuid + "/distribution", item)
        
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

    def _interactive(self, item=None):
        raise NotImplemented
    
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