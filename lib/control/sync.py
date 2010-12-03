# control.sync - Clone system state on local filesystem and synchronize
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import os, json

from util import globals, path
from control.abstract import AbstractController
from control.exceptions import MissingException
from rest.client import Client

class SyncController(AbstractController):

    def __init__(self):
        super(SyncController, self ).__init__()
        self._register(["clone"], self._clone)
        self._register(["h", "help"], self._help)
        self._default_action = self._help
    
    def _clone(self, argv):
        self._options = globals.options
        self._client = Client(self._options.api, self._options.username, self._options.password)
        
        if not self._options.username:
            raise MissingException("Cloning require a username to be defined")
        
        self._root = "cortex." + self._options.username
        self._ensureFolders()
        self._dumpApplications()
        self._dumpDistributions()
        self._dumpOrganizations()

    def _help(self, argv):
        print "Oops, this piece is missing some documentation"
   
    def _ensureFolders(self):
        path.ensure(os.path.join(self._root, "applications"))
        path.ensure(os.path.join(self._root, "distributions"))
        path.ensure(os.path.join(self._root, "organizations"))

                
            
    def _dumpApplications(self):
        result = self._client.read('applications')
        if not (result['count'] == "0"):
            for o in result['items']:
                data = json.dumps(o, sort_keys=True, indent=4)
                name = o['name']
                file = os.path.join(self._root, "applications", name)
                path.ensure(file)
                with open(os.path.join(file, "definition.json"), 'w') as f:
                    f.write(data)               

        
    def _dumpDistributions(self):
        result = self._client.read('distributions')
        if not (result['count'] == "0"):
            for o in result['items']:
                data = json.dumps(o, sort_keys=True, indent=4)
                uuid = o['uuid']
                name = o['name']
                file = os.path.join(self._root, "distributions", name)
                path.ensure(file)
                with open(os.path.join(file, "definition.json"), 'w') as f:
                    f.write(data)               
                try:
                    ks = self._client.read('distributions/' + uuid + "/kickstart.cfg", decode=False)
                    with open(os.path.join(file, "kickstart.template"), 'w') as f:
                        f.write(ks.read())
                except:
                    pass
    
    def _dumpOrganizations(self):
        result = self._client.read('organizations')
        if not (result['count'] == "0"):
            for o in result['items']:
                data = json.dumps(o, sort_keys=True, indent=4)
                uuid = o['uuid']
                name = o['name']
                file = os.path.join(self._root, "organizations", name)
                path.ensure(file)
                with open(os.path.join(file, "definition.json"), 'w') as f:
                    f.write(data)
                self._dumpEnvironments(uuid, file)

    def _dumpEnvironments(self, uuid, root):
        result = self._client.read('environments', parameters={"organizationId":uuid})
        if not (result['count'] == "0"):
            for o in result['items']:
                data = json.dumps(o, sort_keys=True, indent=4)
                uuid = o['uuid']
                name = o['name']
                file = os.path.join(root, name)
                path.ensure(file)
                with open(os.path.join(file, "definition.json"), 'w') as f:
                    f.write(data)
                self._dumpHosts(uuid, file)

    def _dumpHosts(self, uuid, root):
        result = self._client.read('hosts', parameters={"environmentId":uuid})
        if not (result['count'] == "0"):
            for o in result['items']:
                data = json.dumps(o, sort_keys=True, indent=4)
                uuid = o['uuid']
                name = o['name']
                file = os.path.join(root, name)
                path.ensure(file)
                with open(os.path.join(file, "definition.json"), 'w') as f:
                    f.write(data)                    
                self._dumpHostApplications(uuid, file)
                self._dumpHostDistribution(uuid, file)

    def _dumpHostApplications(self, uuid, root):
        file = os.path.join(root, "applications")
        path.ensure(file)
        result = self._client.read('hosts/' + uuid + "/applications")
        if not (result['count'] == "0"):
            for o in result['items']:
                data = json.dumps(o, sort_keys=True, indent=4)
                uuid = o['application']
                application = self._client.read('applications/' + uuid)
                with open(os.path.join(file, application['name'] + ".json"), 'w') as f:
                    f.write(data) 
                    
    def _dumpHostDistribution(self, uuid, root):
        file = os.path.join(root, "distribution")
        path.ensure(file)
        result = self._client.read('hosts/' + uuid + "/distribution")
        data = json.dumps(result, sort_keys=True, indent=4)
        uuid = result['distribution']
        distribution = self._client.read('distributions/' + uuid)
        with open(os.path.join(file, distribution['name'] + ".json"), 'w') as f:
            f.write(data)                                         

    