'''
Created on Nov 18, 2010

@author: eschenal
'''
import optparse, traceback, sys
from control import Controllers
from util import globals 
from control.DefaultController import ControllerException
from control.ProvisionerController import ProvisionerController
from control.OrganizationsController import OrganizationsController
from control.ApplicationsController import ApplicationsController
from control.DistributionsController import DistributionsController
from control.EnvironmentsController import EnvironmentsController
from control.HostsController import HostsController
from control.CmsController import CmsController

def run(argv):
    Controllers.register(["org", "organizations"],  OrganizationsController())
    Controllers.register(["app", "applications"],   ApplicationsController())
    Controllers.register(["dist", "distributions"], DistributionsController())
    Controllers.register(["env", "environments"],   EnvironmentsController())
    Controllers.register(["host", "hosts"],         HostsController())
    Controllers.register(["prov", "provisioner"],   ProvisionerController())
    Controllers.register(["config", "cms", "configuration"],  CmsController())    
    _parse(argv)

def _parse(argv):
            
    usage = "usage: %prog resource [command] [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-A", "--api",    dest="api",      help="endpoint for the API", default="http://localhost:8000/api")
    parser.add_option("-u", "--user",   dest="username", help="username on cortex server",     default="admin")
    parser.add_option("-p", "--pass",   dest="password", help="password on cortex server",     default="secret")
    parser.add_option("-q", "--quiet",  dest="verbose",  help="don't print status messages to stdout", action="store_false", default=True)
    parser.add_option("-f", "--file",   dest="filename", help="input file with a JSON object")
    parser.add_option("-j", "--json",   dest="json",     help="input JSON object")
    parser.add_option("-r", "--raw",    dest="raw",      help="output the raw JSON results", action="store_true", default=False, )
    parser.add_option("--debug",        dest="debug",    help="display debug information", action="store_true", default=False)
    parser.add_option("--org", "--organization", dest="organization",    help="UUID of organization to which this query relates")
    parser.add_option("--env", "--environment",  dest="environment",    help="UUID of environment to which this query relates")
    parser.add_option("--host", "--host",  dest="host",    help="UUID of host to which this query relates")
    
    (globals.options, args) = parser.parse_args()

    if (len(args) == 0):
        parser.print_help()
        exit(-1)  

    _dispatch(args[0], args[1:])
    
def _dispatch(resource, args):
    options = globals.options
    
    try:
        Controllers.dispatch(resource, args)
        exit(0)
    except ControllerException as e:
        print e.msg
        exit(-1)
    except Exception:
        if options.debug:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            exit(-1)
        else :
            print "Oops, it seems something went wrong (use --debug to learn more)."
            exit(-1)
        