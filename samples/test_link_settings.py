# Setup Python path
import sys, test_utils
import definitions as defs
import setup as test_setup
from test_webserver import install_web_server
from test_webserver import wait_changes
from test_simple_web_page import install_simple_web_page, \
    check_page_content, uninstall_simple_web_page
from test_simple_settings import delete_setting, add_simple_setting, update_to_simple_setting, get_simple_setting_json
from test_webserver import uninstall_web_server

sys.path.append("..")


#==============================================================================
# Imports section

import time

from cortex_client.api.api import CortexApi


#==============================================================================
# Script

def get_time_out(argv):
    if len(argv) > 1:
        return int(argv[1])
    else:
        return 0

def get_link_setting_json(key, link, default_value):
    return {"key": key, "link": link, "value": default_value}

def update_to_link_setting(conf, key, link, default):
    setting = conf.settings().get_resource(key)
    setting.set_link(link, default)
    setting.commit()

def add_link_setting(conf, key, link, default_value):
    setting = conf.settings()._new_resource(get_link_setting_json(key, link, default_value))
    setting.create()

def setup(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    install_web_server(host, [get_simple_setting_json("httpd_port", "80")], time_out)
    install_simple_web_page(host, [get_link_setting_json("simple_web_page", "organizations/" + test_setup.global_vars.org_name + "/environments/" + test_setup.global_vars.env_name + "/hosts/" + argv[0] + "/applications/" + test_setup.global_vars.web_server_name + "/settings/httpd_port", "hello")], time_out)

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    check_page_content(host, 80, "/index.html", "Setting value: 80", time_out)

    print "Removing httpd_port setting from WebServer..."
    delete_setting(host.applications().get_resource(test_setup.global_vars.web_server_name), "httpd_port")

    wait_changes(host, time_out)

    check_page_content(host, 80, "/index.html", "Setting value: hello")
    print "Link setting was successfully updated."

    print "Updating link setting of simple web page to simple setting..."
    update_to_simple_setting(host.applications().get_resource(test_setup.global_vars.simple_web_page_name), "simple_web_page", "hello world")

    wait_changes(host, time_out)

    check_page_content(host, 80, "/index.html", "Setting value: hello world", time_out)

    print "Creating simple setting at organization level..."
    add_simple_setting(org, "key", "value")

    print "Creating link setting at environment level..."
    add_link_setting(env, "key", "organizations/" + test_setup.global_vars.org_name + "/settings/key", "")

    print "Updating simple setting of simple web page to link setting..."
    update_to_link_setting(host.applications().get_resource(test_setup.global_vars.simple_web_page_name), "simple_web_page", "organizations/" + test_setup.global_vars.org_name + "/environments/" + test_setup.global_vars.env_name + "/settings/key", "")
    check_page_content(host, 80, "/index.html", "Setting value: value", time_out)

    print "Creating a loop..."
    update_to_link_setting(org, "key", "organizations/" + test_setup.global_vars.org_name + "/environments/" + test_setup.global_vars.env_name + "/hosts/" + argv[0] + "/applications/" + test_setup.global_vars.simple_web_page_name + "/settings/simple_web_page", "default")
    check_page_content(host, 80, "/index.html", "Setting value: default", time_out)

    print "Updating loop..."
    update_to_link_setting(org, "key", "organizations/" + test_setup.global_vars.org_name + "/environments/" + test_setup.global_vars.env_name + "/settings/key", "default2")
    check_page_content(host, 80, "/index.html", "Setting value: default2", time_out)

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    uninstall_simple_web_page(host, time_out)
    uninstall_web_server(host, time_out)

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

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
