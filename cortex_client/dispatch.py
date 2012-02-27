# dispatch.py - Command line dispatching for Cortex. 
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

VERSION = "#VERSION#"
RELEASE = "#RELEASE#"

from control.applications import ApplicationsController
from control.platforms import PlatformsController
from control.distributions import DistributionsController
from control.environments import EnvironmentsController
from control.exceptions import ControllerException, ArgumentException
from control.hosts import HostsController
from control.organizations import OrganizationsController
from control.sync.sync import SyncController
from control.users import UsersController

from rest.exceptions import ApiException
from util import globals
from util.editor import NotModifiedException
import argparse
import traceback
import sys
import textwrap
import control.router
from config import Config, ConfigException
from api.api import CortexApi
from api.exceptions import PythonApiException

def run(argv):
    # resources
    control.router.register(["users"], UsersController())
    control.router.register(["platforms"], PlatformsController())
    control.router.register(["applications"], ApplicationsController())
    control.router.register(["distributions"], DistributionsController())
    control.router.register(["organizations"], OrganizationsController())
    control.router.register(["environments"], EnvironmentsController())
    control.router.register(["hosts"], HostsController())

    # services
    control.router.register(["sync"], SyncController())

    _parse(argv)

def _get_all_options(parser):
    options = []
    for o in parser._option_string_actions:
        options.append(o)
    return options

def _get_value_options(parser):
    # TODO : automatically detect value options
    options = [
                "-f", "--file",
                "-j", "--json",
                "--api",
                "--user",
                "--pass",
                "--templates",
                "--profile",
                "--completions"
                ]
    return options


def __get_parser(config):
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description = "This is the ComodIT CLI.",
                                     epilog = """\
For additional help on a particular (sub)resource, just call the client giving
as argument the resource and/or see man page.

Available resources:
    platforms         Underlying infrastructure platforms
    applications      Recipes to provision and configure applications on a
                      host
    distributions     Recipes to provision and configure distributions on a
                      host
    users             User accounts
    organizations     Top-level organization
    environments      Environment defined within an organization
    hosts             Host defined within an environment
    sync              Synchronization service
""")

    parser.add_argument("resource", help = "A resource")
    parser.add_argument("subresources", help = "Optional subresources", nargs = "*")
    parser.add_argument("action", help = "An action to perform on given (sub)resource", nargs = "?")

    parser.add_argument("-f", "--file", dest = "filename", help = "input file with a JSON object")
    parser.add_argument("-j", "--json", dest = "json", help = "input JSON object via command line")
    parser.add_argument("--raw", dest = "raw", help = "output the raw JSON results", action = "store_true", default = False,)

    parser.add_argument("--skip-chown", dest = "skip_chown", help = "Path to the parent environment", action = "store_true", default = False)
    parser.add_argument("--skip-chmod", dest = "skip_chmod", help = "UUID of the parent environment", action = "store_true", default = False)

    parser.add_argument("--api", dest = "api", help = "endpoint for the API", default = None)
    parser.add_argument("--user", dest = "username", help = "username on cortex server", default = None)
    parser.add_argument("--pass", dest = "password", help = "password on cortex server", default = None)
    parser.add_argument("--templates", dest = "templates_path", help = "directory containing JSON templates", default = config.templates_path)
    parser.add_argument("--profile", dest = "profile_name", help = "Name of profile to use", default = config.get_default_profile_name())

    parser.add_argument("--quiet", dest = "verbose", help = "don't print status messages to stdout", action = "store_false", default = True)
    parser.add_argument("--force", dest = "force", help = "bypass change management and update everything", action = "store_true", default = False)
    parser.add_argument("--debug", dest = "debug", help = "display debug information", action = "store_true", default = False)
    parser.add_argument("--version", dest = "version", help = "display version information", action = "store_true", default = False)

    #parser.add_argument("--options", dest = "show_options", help = "display options", action = "store_true", default = False)
    #parser.add_argument("--options-with-value", dest = "show_options_with_value", help = "display options", action = "store_true", default = False)
    #parser.add_argument("--completions", dest = "param_completions", type = int, help = "parameter to complete", default = -1)

    return parser


def _parse(argv):

    # Load configuration file
    try:
        config = Config()
    except ConfigException, e:
        print "Configuration error:"
        print e.msg
        exit(-1)

    # Create parser
    parser = __get_parser(config)

    # Check for completion related call
    if "--options" in argv:
        for o in _get_all_options(parser):
            print o
        exit(0)

    if "--options-with-value" in argv:
        for o in _get_value_options(parser):
            print o
        exit(0)

    try:
        completions_index = argv.index("--completions")
        del argv[completions_index]
        globals.param_completions = int(argv[completions_index])
        del argv[completions_index]

        if globals.param_completions == 0:
            control.router.print_keywords()
            exit(0)

        globals.param_completions -= 1
    except Exception:
        globals.param_completions = -1

    if "--version" in argv:
        print "ComodIT command line client, version " + VERSION + ", released on " + RELEASE + "."
        exit(0)

    # Parse arguments
    globals.options = parser.parse_known_args(args = argv)[0]

    # Use profile data to configure server API connector. Options provided
    # on command-line have priority.
    profile = config.get_profile(globals.options.profile_name)
    if globals.options.api:
        api = globals.options.api
    else:
        api = profile["api"]
        globals.options.api = api

    if globals.options.username:
        username = globals.options.username
    else:
        username = profile["username"]
        globals.options.username = username

    if globals.options.password:
        password = globals.options.password
    else:
        password = profile["password"]
        globals.options.password = password

    api = CortexApi(api, username, password)

    resource_args = [] + globals.options.subresources

    if not globals.options.action is None:
        resource_args.append(globals.options.action)

    _dispatch(globals.options.resource, resource_args, api)

def _dispatch(resource, args, api):
    options = globals.options

    try:
        control.router.dispatch(resource, api, args)
        exit(0)
    except ControllerException as e:
        print e.msg
    except ArgumentException as e:
        print e.msg
    except ApiException as e:
        print "Error (%s): %s" % (e.code, e.message)
    except PythonApiException as e:
        print e.message
    except NotModifiedException:
        print "Command was canceled since you did not save the file"
    except Exception:
        if options.debug:
            print "Exception in user code."
        else :
            print "Oops, it seems something went wrong (use --debug to learn more)."

    if options.debug:
        print '-' * 60
        traceback.print_exc(file = sys.stdout)
        print '-' * 60
    exit(-1)
