# Setup Python path
import sys, urllib2, test_utils, time
import setup as test_setup
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def wait_changes(host, time_out = 0):
    start_time = time.time()
    while len(host.get_changes()) > 0:
        time.sleep(3)
        now = time.time()

        if time_out > 0 and (now - start_time) > time_out:
            raise Exception("Time-out while waiting for changes")

def test_web_server_default(host, port, time_out = 0):
    wait_changes(host, time_out)
    ip = host.instance().get_single_resource().get_ip("eth0")
    try:
        urllib2.urlopen("http://" + ip + ":" + str(port))
    except urllib2.HTTPError, e:
        if e.code != 403:
            raise Exception("Unexpected HTTP error: " + str(e.code))

def install_web_server(host, settings = [], time_out = 0):
    print "Installing web server..."
    context = host.applications()._new_resource()
    context.set_application(test_setup.global_vars.web_server_name)

    for s in settings:
        if s.has_key("property"):
            context.add_property_setting(s["key"], s["property"])
        elif s.has_key("link"):
            context.add_link_setting(s["key"], s["link"], s["value"])
        elif s.has_key("value"):
            context.add_simple_setting(s["key"], s["value"])

    host.applications().add_resource(context)
    wait_changes(host, time_out)
    print "Web server successfully installed."

def uninstall_web_server(host, time_out = 0):
    print "Uninstalling web server..."
    try:
        host.applications().get_resource(test_setup.global_vars.web_server_name).delete()
        wait_changes(host, time_out)
    except PythonApiException, e:
        print e.message
    print "Web server successfully uninstalled."

def get_time_out(argv):
    if len(argv) > 1:
        return int(argv[1])
    else:
        return 0

def setup(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    install_web_server(host, time_out = time_out)

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    test_web_server_default(host, 80, time_out)

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    uninstall_web_server(host, time_out)

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
