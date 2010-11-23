'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.DefaultController import DefaultController
from util import globals, prompt
from rest.Client import Client
import json
from control.Exceptions import MissingException, NotFoundException

class ResourceController(DefaultController):

    _resource = ""
    _parameters = {}

    def __init__(self):
        super(ResourceController, self ).__init__()
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
    
        # Validate input parameters
        if options.uuid:
            uuid = options.uuid
        elif options.path:
            uuid = self._resolv(options.path)
            if not uuid: raise NotFoundException(uuid)
        else:
            raise MissingException("You must provide a valid object UUID (with --uuid) or path (--path)")
            
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
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + uuid, item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)
    
    def _delete(self, argv):
        options = globals.options
        
        # Validate input parameters
        if options.uuid:
            uuid = options.uuid
        elif options.path:
            uuid = self._resolv(options.path)
            if not uuid: raise NotFoundException(uuid)
        else:
            raise MissingException("You must provide a valid object UUID (with --uuid) or path (--path)")
            
        client = Client(self._endpoint(), options.username, options.password)
        item = client.read(self._resource + "/" + uuid)
        
        if (prompt.confirm(prompt= "Delete " + item['name'] + " ?", resp=False)) :
            client.delete(self._resource + "/" + uuid)
    
    def _render(self, item, detailed=False):
        pass

    def _resolv(self, path):
        pass
                        
    def _endpoint(self):
        options = globals.options
        return options.api