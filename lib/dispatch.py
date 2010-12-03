# dispatch.py - Command line dispatching for Cortex. 
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.
 
VERSION = "0.2-dev"
RELEASE = "Ongoing development"
 
import optparse, traceback, sys, control.router

from control.users import UsersController
from control.applications import ApplicationsController
from control.distributions import DistributionsController
from control.organizations import OrganizationsController
from control.environments import EnvironmentsController
from control.hosts import HostsController
from control.provisioner import ProvisionerController
from control.cms import CmsController
from control.sync import SyncController
from control.exceptions import ControllerException, ArgumentException
from util import globals
from rest.exceptions import ApiException
from util.editor import NotModifiedException

def run(argv):
    control.router.register(["user"], UsersController())
    control.router.register(["app",  "application"], ApplicationsController())
    control.router.register(["dist", "distribution"], DistributionsController())
    control.router.register(["org",  "organization"], OrganizationsController())
    control.router.register(["env",  "environment"], EnvironmentsController())
    control.router.register(["host", "host"], HostsController())
    control.router.register(["prov", "provisioner"], ProvisionerController())
    control.router.register(["cms",  "configuration"], CmsController())        
    control.router.register(["sync"], SyncController())    
    _parse(argv)

def _parse(argv):
            
    usage = "usage: %prog resource [command] [options]"
    parser = optparse.OptionParser(usage)

    parser.add_option("-f", "--file", dest="filename", help="input file with a JSON object")
    parser.add_option("-j", "--json", dest="json",     help="input JSON object via command line")
    parser.add_option("--raw",        dest="raw",      help="output the raw JSON results", action="store_true", default=False,)
    parser.add_option("--with-uuid",  dest="uuid",     help="references are UUID instead of paths",  action="store_true", default=False)
    
    parser.add_option("--org",        dest="org",      help="Path or UUID of the parent organization (conditioned by --with-uuid)")
    parser.add_option("--org-path",   dest="org_path", help="Path to the parent organization")
    parser.add_option("--org-uuid",   dest="org_uuid", help="UUID of the parent organization")

    parser.add_option("--env",        dest="env",      help="Path or UUID of the parent environment (conditioned by --with-uuid)")
    parser.add_option("--env-path",   dest="env_path", help="Path to the parent environment")
    parser.add_option("--env-uuid",   dest="env_uuid", help="UUID of the parent environment")

    parser.add_option("--host",        dest="host",      help="Path or UUID of the parent host (conditioned by --with-uuid)")
    parser.add_option("--host-path",   dest="host_path", help="Path to the parent host")
    parser.add_option("--host-uuid",   dest="host_uuid", help="UUID of the parent host")

    parser.add_option("--api",        dest="api",      help="endpoint for the API",      default="http://localhost:8000/api")
    parser.add_option("--user",       dest="username", help="username on cortex server", default="admin")
    parser.add_option("--pass",       dest="password", help="password on cortex server", default="secret")


    parser.add_option("--quiet",      dest="verbose",  help="don't print status messages to stdout", action="store_false", default=True)
    parser.add_option("--debug",      dest="debug",    help="display debug information", action="store_true", default=False)    
    parser.add_option("--version",    dest="version",    help="display version information", action="store_true", default=False)
    
    (globals.options, args) = parser.parse_args()

    if globals.options.version:
        print "Cortex command line client, version " + VERSION + ", released on " + RELEASE + "."
        exit(0)  

    if (len(args) == 0):
        parser.print_help()
        print_resources()
        exit(-1)

    _dispatch(args[0], args[1:])
    
def _dispatch(resource, args):
    options = globals.options
    
    try:
        control.router.dispatch(resource, args)
        exit(0)
    except ControllerException as e:
        print e.msg
        exit(-1)
    except ArgumentException as e:
        print e.msg
        exit(-1)     
    except ApiException as e:
        print e.message, e.code
        exit(-1)          
    except NotModifiedException:
        print "Command was canceled since you did not save the file"
        exit(-1)       
    except Exception:
        if options.debug:
            print "Exception in user code:"
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
            exit(-1)
        else :
            print "Oops, it seems something went wrong (use --debug to learn more)."
            exit(-1)
        
def print_resources():
    print '''
Resources:
    application         Applications profiles
    distribution        Distribution profiles
    user                User accounts
    organization        Top-level organization
    environment         Environment defined within an organization
    host                Host defined within an environment

Services:
    provisioner         Provision virtual machines based on a host definition
    cms                 Configuration manager
''' 
