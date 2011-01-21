# control.applications - Controller for cortex Applications resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

from control.exceptions import ControllerException, NotFoundException,\
    MissingException
from control.resource import ResourceController
from rest.client import Client
from util import globals
from util.editor import edit_text
import json


class SettingsController(ResourceController):

    _resource = "settings"
    _template = "setting.json"

    def __init__(self):
        super(SettingsController, self ).__init__()

    def _list(self, argv):
        options = globals.options
    
        # Validate input parameters
        if options.host_uuid:
            uuid = options.host_uuid
        elif options.host_path:
            path = options.host_path
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        if options.host and options.uuid:
            uuid = options.host
        elif options.host:
            path = options.host
            uuid = self._resolv(path)
            if not uuid: raise NotFoundException(path)
        else:
            raise MissingException("You must provide a valid host UUID (with --host-uuid) or path (--host-path)")
        
        self._parameters = {"nodeId":uuid}
        
        super(SettingsController, self)._list(argv)   

    def _update(self, argv):
        options = globals.options
          
        client = Client(self._endpoint(), options.username, options.password)
        
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
                uuid = item.get("uuid")
        elif options.json:
            item = json.loads(options.json)
            uuid = item.get("uuid")
        elif len(argv) > 0:
            # Get the uuid/path from the command line
            if options.uuid:
                uuid = argv[0]
            else:
                uuid = self._resolv(argv[0])
                if not uuid: raise NotFoundException(argv[0])
            # Find the resource
            item = client.read(self._resource + "/" + uuid)
            if not item: raise NotFoundException(uuid)
            # Edit the resouce
            original = json.dumps(item, sort_keys=True, indent=4)
            #original = "# To abort the request; just exit your editor without saving this file.\n\n" + original
            updated = edit_text(original)
            #updated = re.sub(r'#.*$', "", updated)
            item = json.loads(updated)
        
        result = client.update(self._resource + "/" + uuid, item, decode=False)

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['key'], item['value']
        else: 
            print "Key:", item['key']
            print "Value:", item['value']
            print "UUID:", item['uuid']

    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']
    
    def _help(self, argv):
        print '''You must provide an action to perfom on this resource. 
        
Actions:
    list            List all settings defined on a node
    show [id]       Show the details of a setting
    add             Add a setting to a node
    update [id]     Update a setting
    delete [id]     Delete a setting
'''