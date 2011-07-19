# control.resource - Generic controller for managing cortex resources. 
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import json, os

from control.abstract import AbstractController
from util import globals, prompt, fileupload
from rest.client import Client
from control.exceptions import NotFoundException, MissingException
from util.editor import edit_text
import re
import urlparse

TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates'))

class FilesController(AbstractController):

    _resource = "files"
    _template = ""
    _parameters = {}

    def __init__(self):
        super(FilesController, self).__init__()
        self._register(["l", "list"], self._list)   
        self._register(["s", "show"], self._show)
        self._register(["g", "get"], self._get)
        self._register(["a", "add"], self._add)
        self._register(["u", "update"], self._update)        
        self._register(["d", "delete"], self._delete)
        self._register(["h", "help"], self._help)
        self._default_action = self._help
        
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

    def _get(self, argv):
        options = globals.options
    
        # Require an object as argument
        if len(argv) == 0:
            raise MissingException("You must provide a valid object identifier")
    
        # Validate input parameters
        uuid = argv[0]
            
        # Query the server
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid, decode=False)
        
        # Display the result
        for line in result:
                print line,
    
    def _show(self, argv):
        options = globals.options
    
        # Require an object as argument
        if len(argv) == 0:
            raise MissingException("You must provide a valid object identifier")
    
        # Validate input parameters
        uuid = argv[0]
            
        # Query the server
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read(self._resource + "/" + uuid + "/_meta")
        
        # Display the result
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result, detailed=True)
    
    def _add(self, argv):
        options = globals.options
       
        if not options.filename:
            raise MissingException("You must provide a file to upload (--file)")
        
        with open(options.filename, 'r') as f:
            url = urlparse.urlparse(self._endpoint() + "/" + self._resource)
            response = fileupload.post_multipart(url.netloc, url.path, [("test", "none")], [("file", options.filename, f.read())], {"Authorization": "Basic " + (options.username + ":" + options.password).encode("base64").rstrip()})

        result = json.loads(response);
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else: 
            if (len(result) == "0"):
                print "Request returned 0 object."
            else:
                for o in result:
                    print o
    
    def _update(self, argv):
        options = globals.options

        if len(argv) == 0:
            raise MissingException("You must provide a valid object identifier")
        uuid = argv[0]
                  
        if not options.filename:
            raise MissingException("You must provide a file to upload (--file)")
        
        with open(options.filename, 'r') as f:
            url = urlparse.urlparse(self._endpoint() + "/" + self._resource + "/" + uuid)
            response = fileupload.post_multipart(url.netloc, url.path, [("test", "none")], [("file", options.filename, f.read())], {"Authorization": "Basic " + (options.username + ":" + options.password).encode("base64").rstrip()})
        
        result = json.loads(response);
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else: 
            if (result['count'] == "0"):
                print "Request returned 0 object."
            else:
                for o in result['items']:
                    self._render(o)
    
    def _delete(self, argv):
        options = globals.options
        
        # Require an object as argument
        if len(argv) == 0:
            raise MissingException("You must provide a valid object identifier")
    
        # Validate input parameters
        uuid = argv[0]
            
        client = Client(self._endpoint(), options.username, options.password)
        item = client.read(self._resource + "/" + uuid + "/_meta")
        
        if (prompt.confirm(prompt="Delete " + item['name'] + " ?", resp=False)) :
            client.delete(self._resource + "/" + uuid)
    
    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else: 
            print "Name:", item['name']
            print "UUID:", item['uuid']

    
    def _resolv(self, path):
        pass
                        
    def _endpoint(self):
        options = globals.options
        return options.api
    
    def _help(self, argv):
        print '''You must provide an action to perfom on this resource. 
        
Actions:
    list            List all files available to the user
    show [uuid]     Show the details of a file
    get [uuid]      Fetch the content of a file
    add             Upload a new file
    update [uuid]   Update the content of a file
    delete [uuid]   Delete a file
'''
