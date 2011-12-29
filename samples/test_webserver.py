# Setup Python path
import sys, urllib2, test_utils
import definitions as defs
import setup as test_setup
sys.path.append("..")


#==============================================================================
# Imports section

import time

from cortex_client.api.api import CortexApi
from cortex_client.api.contexts import ApplicationContext
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def test_web_server_default(host, port):
    while len(host.get_changes()) > 0:
        time.sleep(3)
    try:
        urllib2.urlopen("http://" + host.get_instance().get_ip() + ":" + str(port))
    except urllib2.HTTPError, e:
        if e.code != 403:
            raise Exception("Unexpected HTTP error: " + str(e.code))

def setup():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    print "Installing web server..."
    context = ApplicationContext()
    context.set_application(defs.global_vars.app_name)
    host.install_application(context)
    while len(host.get_changes()) > 0:
        time.sleep(3)

def run():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    test_web_server_default(host, 80)

    print "Web server was successfully installed."

def tear_down():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    print "Uninstalling web server..."
    try:
        host.uninstall_application(defs.global_vars.app_name)
        while len(host.get_changes()) > 0:
            time.sleep(3)
    except PythonApiException, e:
        print e.message

    print "Web server was successfully uninstalled."

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
