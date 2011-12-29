# Setup Python path
import sys, test_utils
import definitions as defs
import setup as test_setup
from test_webserver import test_web_server_default
sys.path.append("..")


#==============================================================================
# Imports section

import time

from cortex_client.api.api import CortexApi
from cortex_client.api.contexts import ApplicationContext
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def __get_httpd_port_json(port):
    return {"key": "httpd_port", "value": str(port)}

def __set_httpd_port_setting(conf, host, port):
    setting = conf.settings()._new_resource(__get_httpd_port_json(port))
    setting.create()
    test_web_server_default(host, port)

def __update_httpd_port_setting(conf, host, port):
    setting = conf.settings().get_resource("httpd_port")
    setting.set_value(str(port))
    setting.commit()
    test_web_server_default(host, port)

def __set_httpd_port_setting_at_app(host, port):
    setting = host.application_settings(defs.global_vars.app_name)._new_resource(__get_httpd_port_json(port))
    setting.create()
    test_web_server_default(host, port)

def __unset_httpd_port_setting(host, conf):
    try:
        setting = conf.settings().get_resource("httpd_port")
        setting.delete()
    except PythonApiException, e:
        print e.message

def __unset_httpd_port_setting_at_app(host):
    try:
        setting = host.application_settings().get_resource("httpd_port")
        setting.delete()
    except PythonApiException, e:
        print e.message

def __unset_httpd_port_setting_and_test(conf, host, port):
    setting = conf.settings().get_resource("httpd_port")
    setting.delete()
    test_web_server_default(host, port)

def __unset_httpd_port_setting_at_app_and_test(host, port):
    setting = host.application_settings(defs.global_vars.app_name).get_resource("httpd_port")
    setting.delete()
    test_web_server_default(host, port)

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

    print "Setting httpd_port at organization level..."
    __set_httpd_port_setting(org, host, 80)

    print "Setting httpd_port at environment level..."
    __set_httpd_port_setting(env, host, 88)

    print "Setting httpd_port at host level..."
    __set_httpd_port_setting(host, host, 8000)

    print "Setting httpd_port at application level..."
    __set_httpd_port_setting_at_app(host, 8888)

    print "Unsetting httpd_port at application level..."
    __unset_httpd_port_setting_at_app_and_test(host, 8000)

    print "Unsetting httpd_port at host level..."
    __unset_httpd_port_setting_and_test(host, host, 88)

    print "Unsetting httpd_port at environment level..."
    __unset_httpd_port_setting_and_test(env, host, 80)

    print "Unsetting httpd_port at organization level..."
    __unset_httpd_port_setting_and_test(org, host, 80)

    print "Setting httpd_port at host level..."
    __set_httpd_port_setting(host, host, 8000)

    print "Changing httpd_port at host level..."
    __update_httpd_port_setting(host, host, 80)

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

    print "Removing httpd_port from organization..."
    __unset_httpd_port_setting(host, org)

    print "Removing httpd_port from environment..."
    __unset_httpd_port_setting(host, env)

    print "Removing httpd_port from host..."
    __unset_httpd_port_setting(host, host)

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
