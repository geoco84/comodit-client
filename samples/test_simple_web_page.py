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

def test_web_server_page(host, port, page):
    wait_changes(host)
    ip = host.instance().get_single_resource().get_ip("eth0")
    try:
        return urllib2.urlopen("http://" + ip + ":" + str(port) + page)
    except urllib2.HTTPError, e:
        raise Exception("Unexpected HTTP error: " + str(e.code))

def install_simple_web_page(host, settings):
    print "Installing simple web page..."
    context = host.applications()._new_resource()
    context.set_application(defs.global_vars.simple_web_page_name)

    for s in settings:
        context.add_setting(s["key"], s["value"])

    host.applications().add_resource(context)
    wait_changes(host)
    print "Simple web page successfully installed."

def uninstall_simple_web_page(host):
    print "Uninstalling simple web page..."
    try:
        host.applications().get_resource(defs.global_vars.simple_web_page_name).delete()
        wait_changes(host)
    except PythonApiException, e:
        print e.message
    print "Simple web page successfully installed."

def check_page_content(host, port, page, value):
    content_reader = test_web_server_page(host, port, page)
    content = content_reader.read()
    if content.find("Setting value: " + value) == -1:
        raise Exception("Unexpected page content")

def get_setting_json(key, value):
    return {"key": key, "value": value}

def setup():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    install_web_server(host, [get_setting_json("httpd_port", "80")])
    install_simple_web_page(host, [get_setting_json("simple_web_page", "simple://hello")])

def run():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    check_page_content(host, 80, "/index.html", "hello")

def tear_down():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    uninstall_web_server(host)
    uninstall_simple_web_page(host)

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
