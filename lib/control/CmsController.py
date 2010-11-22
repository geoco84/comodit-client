'''
Created on Nov 22, 2010

@author: eschenal
'''
from util import globals
from control.DefaultController import DefaultController
from rest.Client import Client
import subprocess

class CmsController(DefaultController):

    _resource = "config"

    def __init__(self):
        super(CmsController, self ).__init__()
        self._register(["apply"], self._apply)
    
    def _apply(self, argv):
        options = globals.options
        
        if not options.host:
            print "You must provide the UUID of the host"
            exit(-1)
        else :
            host = options.host
    
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("hosts/" + host)
        
        hostname = result.get('hostname')
        domain = result.get('domain')
        fqdn = hostname + "." + domain
        
        subprocess.check_call(["ssh", "root@puppet-comodit.angleur", "puppetrun --host " + fqdn], stderr=subprocess.STDOUT)
        
    def _endpoint(self):
        options = globals.options
        return options.api