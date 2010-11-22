'''
Created on Nov 22, 2010

@author: eschenal
'''
from util import globals
from control.DefaultController import DefaultController, ControllerException
from rest.Client import Client
import json

class HostApplicationsController(DefaultController):

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
    
        if not options.host:
            print "You must provide the UUID of the host"
            exit(-1)
        else :
            host = options.host
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + host + "/applications")
        
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
    
        if not options.host:
            print "You must provide the UUID of the host"
            exit(-1)
        else :
            host = options.host
    
        if (len(argv) == 0):
            print "You must provide the UUID of the application to delete."
            exit(-1)
        else:
            uuid = argv[0]
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + host + "/applications/" + uuid)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)

    def _add(self, argv):
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
            raise ControllerException("Adding an application is not possible in interactive mode.")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.create(self._resource + "/" + host + "/applications/", item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
            
    def _update(self, argv):
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
            raise ControllerException("Configuring an application is not possible in interactive mode.")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + host + "/applications/" + item['application'], item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
        
    def _remove(self, argv):
        options = globals.options
          
        if not options.host:
            print "You must provide the UUID of the host"
            exit(-1)
        else:    
            host = options.host 
          
    
        if (len(argv) == 0):
            print "You must provide the UUID of the application to delete."
            exit(-1)
        else:
            uuid = argv[0]
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.delete(self._resource + "/" + host + "/applications/" + uuid)
    
    def _render(self, item, detailed=False):
            
        print item["application"]
        if item.has_key('settings'):
            for setting in item['settings']:
                print "    %-30s: %s" % (setting['key'], setting['value'])

    def _interactive(self, item=None):
        raise NotImplemented
    
    def _endpoint(self):
        options = globals.options
        return options.api