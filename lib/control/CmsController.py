'''
Created on Nov 22, 2010

@author: eschenal
'''
from util import globals
from control.DefaultController import DefaultController
from rest.Client import Client
import subprocess
from control.Exceptions import NotFoundException, MissingException,\
    ArgumentException

class CmsController(DefaultController):

    _resource = "config"

    def __init__(self):
        super(CmsController, self ).__init__()
        self._register(["apply"], self._apply)
    
    def _apply(self, argv):
        options = globals.options
        
        # Validate input parameters
        if options.uuid:
            uuid = options.uuid
        elif options.path:
            uuid = self._resolv(options.path)
            if not uuid: raise NotFoundException(uuid)
        else:
            raise MissingException("You must provide a valid host UUID (with --uuid) or path (--path)")
    
        if isinstance(uuid, (list, tuple)):
            for u in uuid:
                self._puppet(u)
        else:
            self._puppet(uuid)

        
    def _endpoint(self):
        options = globals.options
        return options.api
    
    def _puppet(self, uuid):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("hosts/" + uuid)
        
        hostname = result.get('hostname')
        domain = result.get('domain')
        fqdn = hostname + "." + domain
        print "Running puppet on " + fqdn
        subprocess.check_call(["ssh", "root@puppet-comodit.angleur", "puppetrun --host " + fqdn], stderr=subprocess.STDOUT)
    
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if not result.has_key('uuid') : return None
        
        if result.get('nature') == 'host':
            return result.get('uuid')
        elif result.get('nature') == 'environment':
            return self._hosts(result.get('uuid'))
        else:
            raise ArgumentException("Cannot apply configuration on a whole domain.")
    
    def _hosts(self, uuid):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("hosts", parameters={"environmentId": uuid})
        if result.get('count') > 0 :
            uuids = []
            for host in result.get('items'):
                uuids.append(host.get('uuid'))
            return uuids