# control.applications - Controller for cortex Applications resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

from control.exceptions import ControllerException
from control.resource import ResourceController
from rest.client import Client
from util import globals
import json


class ApplicationsController(ResourceController):

    _resource = "applications"
    _template = "application.json"

    def __init__(self):
        super(ApplicationsController, self ).__init__()

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else: 
            print "Name:", item['name']
            if item.has_key('description'): print "Description:", item['description']
            print "UUID:", item['uuid']
            if item.has_key('packages'):
                print "Packages:"
                for p in item.get('packages'):
                    print "   ", p                 
            if item.has_key('parameters'):
                print "Parameters:"
                for p in item.get('parameters'):
                    print "   ", p.get('key')


    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/application/" + path)
        if result.has_key('uuid') : return result['uuid']         