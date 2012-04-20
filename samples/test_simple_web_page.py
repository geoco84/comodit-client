# Setup Python path
import sys, urllib2, test_utils
import definitions as defs
import setup as test_setup
from test_webserver import wait_changes, install_web_server, uninstall_web_server

sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def test_web_server_page(host, port, page, time_out = 0):
    wait_changes(host, time_out)
    ip = host.instance().get_single_resource().get_ip("eth0")
    try:
        return urllib2.urlopen("http://" + ip + ":" + str(port) + page)
    except urllib2.HTTPError, e:
        raise Exception("Unexpected HTTP error: " + str(e.code))
    except urllib2.URLError, e:
        raise Exception("Unexpected URL error: " + str(e.reason))

def install_simple_web_page(host, settings, time_out = 0):
    print "Installing simple web page..."
    context = host.applications()._new_resource()
    context.set_application(test_setup.global_vars.simple_web_page_name)

    for s in settings:
        if s.has_key("property"):
            context.add_property_setting(s["key"], s["property"])
        elif s.has_key("link"):
            context.add_link_setting(s["key"], s["link"], s["value"])
        elif s.has_key("value"):
            context.add_simple_setting(s["key"], s["value"])

    host.applications().add_resource(context)
    wait_changes(host, time_out)
    print "Simple web page successfully installed."

def uninstall_simple_web_page(host, time_out = 0):
    print "Uninstalling simple web page..."
    try:
        host.applications().get_resource(test_setup.global_vars.simple_web_page_name).delete()
        wait_changes(host, time_out)
    except PythonApiException, e:
        print e.message
    print "Simple web page successfully installed."

def check_page_content(host, port, page, value, time_out = 0):
    content_reader = test_web_server_page(host, port, page, time_out)
    content = content_reader.read()
    if content.find(value) == -1:
        raise Exception("Unexpected page content")

def get_simple_setting_json(key, value):
    return {"key": key, "value": value}

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

    install_web_server(host, [get_simple_setting_json("httpd_port", "80")], time_out)
    install_simple_web_page(host, [get_simple_setting_json("simple_web_page", "hello")], time_out)

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    check_page_content(host, 80, "/index.html", "Setting value: hello", time_out)

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    uninstall_web_server(host, time_out)
    uninstall_simple_web_page(host, time_out)

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
