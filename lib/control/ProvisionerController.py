'''
Created on Nov 22, 2010

@author: eschenal
'''
from util import globals
from control.DefaultController import DefaultController, ControllerException
from rest.Client import Client
import json

class ProvisionerController(DefaultController):

    _resource = "provisioner"

    def __init__(self):
        super(ProvisionerController, self ).__init__()
        self._register(["ks", "kickstart"], self._kickstart)
        self._register(["create"], self._provision)
    
    def _kickstart(self, argv):
        options = globals.options
        
        if not options.host:
            print "You must provide the UUID of the host"
            exit(-1)
        else :
            host = options.host
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/kickstart.cfg", parameters={"hostId":host}, decode=False)
        print result.read()
        

    def _provision(self, argv):
        options = globals.options
        
        if not options.host:
            print "You must provide the UUID of the host"
            exit(-1)
        else :
            host = options.host
            
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/_provision", parameters={"hostId":host}, decode=False)
        print result.read()   

    
    def _set(self, argv):
        options = globals.options
          
        if not options.host:
            print "You must provide the UUID of the host"
            exit(-1)
        else:    
            host = options.host 
          
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
        elif options.json:
            item = json.loads(options.json)
        else:
            raise ControllerException("Setting a distribution is not possible in interactive mode.")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + host + "/distribution", item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
        
    def _render(self, item, detailed=False):
        if item.has_key('settings'):
            for setting in item['settings']:
                print "%-30s: %s" % (setting['key'], setting['value'])

    def _interactive(self, item=None):
        raise NotImplemented
    
    def _endpoint(self):
        options = globals.options
        return options.api