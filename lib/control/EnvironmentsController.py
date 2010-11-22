'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.ResourceController import ResourceController
from util import globals, prompt

class EnvironmentsController(ResourceController):

    _resource = "environments"

    def __init__(self):
        super(EnvironmentsController, self ).__init__()
        
    def _pre(self, argv):
        options = globals.options
        self._parameters = {"organizationId":options.organization}
        
    def _render(self, item, detailed=False):
        print item['name'], item['uuid']

    def _interactive(self, item=None):
        name = None
        description = None
        
        if not item: item = {}
        options = globals.options
        
        if item.has_key('organization'):
            organization = item['organization']
        elif options.organization:
            organization = options.organization
            
        if item.has_key('name'):
            name = item['name']
        
        if item.has_key('description'):
            description = item['description']

        item['organization'] = prompt.raw_input_default("Organization: ", organization)    
        item['name'] = prompt.raw_input_default('Name: ', name)
        desc = prompt.raw_input_default("Description: ", description)
        if len(desc) > 0:
            item['description'] = desc
        
        return item