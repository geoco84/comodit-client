'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.ResourceController import ResourceController
from util import globals, prompt
from control.HostDistributionController import HostDistributionController
from control.HostApplicationsController import HostApplicationsController

class HostsController(ResourceController):

    _resource = "hosts"

    def __init__(self):
        super(HostsController, self ).__init__()
        self._register(["dist", "distribution"], self._distribution)
        self._register(["apps", "applications"], self._applications)
        
    def _pre(self, argv):
        options = globals.options
        self._parameters = {"environmentId":options.environment}
        
    def _render(self, item, detailed=False):
        print item['uuid'], item['name']

    def _distribution(self, argv):
        controller = HostDistributionController()
        controller.run(argv)
        
    def _applications(self, argv):
        controller = HostApplicationsController()
        controller.run(argv)        

    def _interactive(self, item=None):
        if not item: item = {}
        options = globals.options
        name = None
        description = None
        environment = None
        hostname = None
        domain = None
        
        if item.has_key('environment'):
            environment = item['environment']
        elif options.environment:
            environment = options.environment
        item['environment'] = prompt.raw_input_default("Environment: ", environment)
            
        if item.has_key('name'):
            name = item['name']
        item['name'] = prompt.raw_input_default('Name: ', name)
                
        if item.has_key('hostname'):
            hostname = item['hostname']            
        item['hostname'] = prompt.raw_input_default('Hostname: ', hostname)

        if item.has_key('domain'):
            domain = item['domain']            
        item['domain'] = prompt.raw_input_default('Domain name: ', domain)
    
        if item.has_key('description'):
            description = item['description']
        desc = prompt.raw_input_default("Description: ", description)
        if len(desc) > 0:
            item['description'] = desc
        
        return item