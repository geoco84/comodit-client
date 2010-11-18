'''
Created on Nov 18, 2010

@author: eschenal
'''
from pprint import pprint

import api, globals, prompt
import json

def run(args):
    
    if (len(args) == 0):
        _list()
    elif (args[0] in ["l", "list"]):
        _list()
    elif (args[0] in ["s", "show"]):
        _show(args[1:])
    elif (args[0] in ["a", "add"]):
        _add()
    elif (args[0] in ["m", "modify"]):
        _update(args[1:])
    elif (args[0] in (["d", "delete"])):
        _delete(args[1:])
    else:
        _usage()
        exit(-1)
        
def _list():
    options = globals.options
    client = api.Client(_endpoint(), options.username, options.password)
    result = client.list("organizations")
    
    if options.raw:
        print json.dumps(result, sort_keys=True, indent=4)
    else: 
        if (result['count'] == 0):
            print "You don't have any organization yet."
        else:
            for o in result['items']:
                _print(o)
            
def _show(args):
    options = globals.options
    
    if (len(args) == 0):
        print "You must provide the UUID of the organization to show."
        exit(-1)
    
    client = api.Client(_endpoint(), options.username, options.password)
    result = client.read("organizations", args[0])
    
    if options.raw:
        print json.dumps(result, sort_keys=True, indent=4)
    else:
        _print(result)
        
def _add():
    options = globals.options
   
    if options.filename:
        with open(options.filename, 'r') as f:
            organization = json.load(f)
    elif options.json:
        organization = json.loads(options.json)            
    else:
        organization = {}
        organization['name'] = raw_input('Name: ')
        desc = raw_input("Description: ")
        if len(desc) > 0:
            organization['description'] = desc
    
    client = api.Client(_endpoint(), options.username, options.password)
    result = client.create("organizations", organization)
    
    if options.raw:
        print json.dumps(result, sort_keys=True, indent=4)
    else:
        _print(result)

def _update(args):
    options = globals.options
      
    client = api.Client(_endpoint(), options.username, options.password)
    
    if options.filename:
        with open(options.filename, 'r') as f:
            organization = json.load(f)
            uuid = organization.get("uuid")
    elif options.json:
        organization = json.loads(options.json)
        uuid = organization.get("uuid")
    else:
        if (len(args) == 0):
            print "You must provide the UUID of the organization to show."
            exit(-1)
        
        uuid = args[0]
        organization = client.read("organizations", uuid)
        
        name = prompt.raw_input_default("Name: ", organization.get('name'))
        if name: organization['name'] = name
     
        desc = prompt.raw_input_default("Description: ", organization.get('description'))
        if desc: organization['description'] = desc
    
    client = api.Client(_endpoint(), options.username, options.password)
    result = client.update("organizations", uuid, organization)
    
    if options.raw:
        print json.dumps(result, sort_keys=True, indent=4)
    else:
        _print(result)

def _delete(args):
    options = globals.options
    
    if (len(args) == 0):
        print "You must provide the UUID of the organization to delete."
        exit(-1)
        
    client = api.Client(_endpoint(), options.username, options.password)
    organization = client.read("organizations", args[0])
    
    if (prompt.confirm(prompt= "Delete the " + organization['name'] + " organization ?", resp=False)) :
        client.delete("organizations", args[0])
    

def _print(org):
    print org['uuid']
    print " ", org['name']
    if (org.has_key('description')): 
        print " ", org['description']

def _endpoint():
    options = globals.options
    return "http://" + options.host.rstrip(("/")) + ":" + options.port + "/api/"

def _usage():
        print """ACTIONS:
 list \t\t List all domains owned by the authenticated user 
 show UUID \t Return a specific domain (based on UUID)
 add \t\t Create a new domain
 update \t Update a domain
 delete UUID \t Delete the specified domain 
"""

