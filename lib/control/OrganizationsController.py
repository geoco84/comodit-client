'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.ResourceController import ResourceController
from util import prompt

class OrganizationsController(ResourceController):

    _resource = "organizations"

    def __init__(self):
        super(OrganizationsController, self ).__init__()

    def _render(self, item, detailed=False):
        print item['uuid'], item['name']
        
        if detailed:
            if item.has_key('description'):
                print "   ", item['description']
        

    def _interactive(self, item=None):
        if not item: item = {}
        
        item['name'] = prompt.raw_input_default('Name: ', item.get('name'))
        desc = prompt.raw_input_default("Description: ", item.get('description'))
        if len(desc) > 0:
            item['description'] = desc
        
        return item