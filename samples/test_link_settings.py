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
from cortex_client.api.settings import Setting


#==============================================================================
# Script

def test_web_server_page(host, port, page):
    while len(host.get_changes()) > 0:
        time.sleep(3)
    try:
        return urllib2.urlopen("http://" + host.get_instance().get_ip() + ":" + str(port) + page)
    except urllib2.HTTPError, e:
        raise Exception("Unexpected HTTP error: " + str(e.code))

def setup():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    print "Installing web server..."
    context = ApplicationContext()
    context.set_application(defs.global_vars.web_server_name)
    context.add_setting(Setting(None, {"key":"httpd_port", "value":"simple://80"}))
    host.install_application(context)
    while len(host.get_changes()) > 0:
        time.sleep(3)

    print "Installing simple web page with linked setting..."
    context = ApplicationContext()
    context.set_application(defs.global_vars.simple_web_page_name)
    context.add_setting(Setting(None, {"key":"simple_web_page",
                                 "value":"link://organizations/" + defs.global_vars.org_name + "/environments/" + defs.global_vars.env_name + "/hosts/" + defs.global_vars.host_name + "/applications/" + defs.global_vars.web_server_name + "/settings/httpd_port:hello"}))
    host.install_application(context)
    while len(host.get_changes()) > 0:
        time.sleep(3)

def run():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    content_reader = test_web_server_page(host, 80, "/index.html")
    content = content_reader.read()
    if content.find("Setting value: 80") == -1:
        raise Exception("Unexpected page content")

    print "Link setting has expected value."

    print "Removing httpd_port setting from WebServer..."
    s = host.application_settings(defs.global_vars.web_server_name).get_resource("httpd_port")
    s.delete()

    while len(host.get_changes()) > 0:
        time.sleep(3)

    content_reader = test_web_server_page(host, 80, "/index.html")
    content = content_reader.read()
    if content.find("Setting value: hello") == -1:
        raise Exception("Unexpected page content")

    print "Link setting was successfully updated."

    print "Updating link setting of simple web page to simple setting..."
    s = host.application_settings(defs.global_vars.simple_web_page_name).get_resource("simple_web_page")
    s.set_value("simple://hello world")
    s.commit()

    while len(host.get_changes()) > 0:
        time.sleep(3)

    content_reader = test_web_server_page(host, 80, "/index.html")
    content = content_reader.read()
    if content.find("Setting value: hello world") == -1:
        raise Exception("Unexpected page content")

def tear_down():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    print "Uninstalling simple web page..."
    try:
        host.uninstall_application(defs.global_vars.simple_web_page_name)
        while len(host.get_changes()) > 0:
            time.sleep(3)
    except PythonApiException, e:
        print e.message

    print "Uninstalling web server..."
    try:
        host.uninstall_application(defs.global_vars.web_server_name)
        while len(host.get_changes()) > 0:
            time.sleep(3)
    except PythonApiException, e:
        print e.message

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
