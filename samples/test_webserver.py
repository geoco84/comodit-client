# Setup Python path
import sys, urllib2, test_utils
import definitions as defs
import setup as test_setup
sys.path.append("..")


#==============================================================================
# Imports section

import time

from cortex_client.api.api import CortexApi
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def wait_changes(host):
    while len(host.get_changes()) > 0:
        time.sleep(3)

def test_web_server_default(host, port):
    wait_changes(host)
    ip = host.instance().get_single_resource().get_ip("eth0")
    try:
        urllib2.urlopen("http://" + ip + ":" + str(port))
    except urllib2.HTTPError, e:
        if e.code != 403:
            raise Exception("Unexpected HTTP error: " + str(e.code))

def install_web_server(host, settings = []):
    print "Installing web server..."
    context = host.applications()._new_resource()
    context.set_application(defs.global_vars.web_server_name)

    for s in settings:
        context.add_setting(s["key"], s["value"])

    host.applications().add_resource(context)
    wait_changes(host)
    print "Web server successfully installed."

def uninstall_web_server(host):
    print "Uninstalling web server..."
    try:
        host.applications().get_resource(defs.global_vars.web_server_name).delete()
        wait_changes(host)
    except PythonApiException, e:
        print e.message
    print "Web server successfully uninstalled."

def setup():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    install_web_server(host)

def run():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    test_web_server_default(host, 80)

def tear_down():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    uninstall_web_server(host)

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
