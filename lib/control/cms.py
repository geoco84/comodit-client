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

    _resource = "cms"

    def __init__(self):
        super(CmsController, self ).__init__()
        self._register(["apply"], self._apply)
    
    def _apply(self, argv):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/_apply", decode=False)
        
    def _endpoint(self):
        options = globals.options
        return options.api
    
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if not result.has_key('uuid') : return None
        
        if result.get('nature') == 'host':
            return result.get('uuid')
        raise ArgumentException("Cannot apply (yet) configuration on more than one host at a time.")
    