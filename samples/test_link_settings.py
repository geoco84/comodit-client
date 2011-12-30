# Setup Python path
import sys, test_utils
import definitions as defs
import setup as test_setup
from test_webserver import install_web_server
from test_simple_web_page import get_setting_json
from test_simple_web_page import install_simple_web_page, \
    check_page_content, uninstall_simple_web_page
from test_simple_settings import delete_setting, update_setting, \
    add_setting
from test_webserver import uninstall_web_server
sys.path.append("..")


#==============================================================================
# Imports section

import time

from cortex_client.api.api import CortexApi


#==============================================================================
# Script

def setup():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    install_web_server(host, [get_setting_json("httpd_port", "simple://80")])
    install_simple_web_page(host, [get_setting_json("simple_web_page", "link://organizations/" + defs.global_vars.org_name + "/environments/" + defs.global_vars.env_name + "/hosts/" + defs.global_vars.host_name + "/applications/" + defs.global_vars.web_server_name + "/settings/httpd_port:hello")])

def run():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    check_page_content(host, 80, "/index.html", "80")

    print "Removing httpd_port setting from WebServer..."
    delete_setting(host.applications().get_resource(defs.global_vars.web_server_name), "httpd_port")

    while len(host.get_changes()) > 0:
        time.sleep(3)

    check_page_content(host, 80, "/index.html", "hello")
    print "Link setting was successfully updated."

    print "Updating link setting of simple web page to simple setting..."
    update_setting(host.applications().get_resource(defs.global_vars.simple_web_page_name), "simple_web_page", "simple://hello world")

    while len(host.get_changes()) > 0:
        time.sleep(3)

    check_page_content(host, 80, "/index.html", "hello world")

    print "Creating simple setting at organization level..."
    add_setting(org, "key", "simple://value")

    print "Creating link setting at environment level..."
    add_setting(env, "key", "link://organizations/" + defs.global_vars.org_name + "/settings/key")

    print "Updating simple setting of simple web page to link setting..."
    update_setting(host.applications().get_resource(defs.global_vars.simple_web_page_name), "simple_web_page", "link://organizations/" + defs.global_vars.org_name + "/environments/" + defs.global_vars.env_name + "/settings/key")

    while len(host.get_changes()) > 0:
        time.sleep(3)

    check_page_content(host, 80, "/index.html", "value")

    print "Creating a loop..."
    update_setting(org, "key", "link://organizations/" + defs.global_vars.org_name + "/environments/" + defs.global_vars.env_name + "/hosts/" + defs.global_vars.host_name + "/applications/" + defs.global_vars.simple_web_page_name + "/settings/simple_web_page:default")
    check_page_content(host, 80, "/index.html", "default")

    print "Updating loop..."
    update_setting(org, "key", "link://organizations/" + defs.global_vars.org_name + "/environments/" + defs.global_vars.env_name + "/settings/key:default2")

    while len(host.get_changes()) > 0:
        time.sleep(3)

    check_page_content(host, 80, "/index.html", "default2")

def tear_down():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    uninstall_simple_web_page(host)
    uninstall_web_server(host)

    print "Removing setting at organization level..."
    try:
        delete_setting(org, "key")
    except Exception, e:
        print e.message

    print "Creating link setting at environment level..."
    try:
        delete_setting(env, "key")
    except Exception, e:
        print e.message

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
