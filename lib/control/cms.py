# control.sync - Clone system state on local filesystem and synchronize
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import subprocess

from util import globals
from control.abstract import AbstractController
from control.exceptions import NotFoundException, MissingException,\
    ArgumentException
from rest.client import Client

class CmsController(AbstractController):

    _resource = "config"

    def __init__(self):
        super(CmsController, self ).__init__()
        self._register(["apply"], self._apply)
    
    def _apply(self, argv):
        options = globals.options
        
        # Require an object as argument
        if len(argv) == 0:
            raise MissingException("You must provide a valid host UUID or path as argument")
    
        # Validate input parameters
        if options.uuid:
            uuid = argv[0]
        else:
            uuid = self._resolv(argv[0])
            if not uuid: raise NotFoundException(uuid)
    
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
        print "Running CMS on " + fqdn
        subprocess.check_call(["ssh", "root@puppet-comodit.angleur", "puppetrun --host " + fqdn], stderr=subprocess.STDOUT)
    
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if not result.has_key('uuid') : return None
        
        if result.get('nature') == 'host':
            return result.get('uuid')
        raise ArgumentException("Cannot apply (yet) configuration on more than one host at a time.")
    