'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.ResourceController import ResourceController
from rest.Client import Client
from util import prompt, globals

class OrganizationsController(ResourceController):

    _resource = "organizations"

    def __init__(self):
        super(OrganizationsController, self ).__init__()

    def _render(self, item, detailed=False):
        print item['uuid'], item['name']
        
        if detailed:
            if item.has_key('description'):
                print "   ", item['description']
        

    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']