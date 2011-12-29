# Setup Python path
import sys, setup, urllib2
import definitions as defs
sys.path.append("..")


#==============================================================================
# Imports section

import time

from cortex_client.api.api import CortexApi
from cortex_client.api.contexts import ApplicationContext


#==============================================================================
# Script

def __get_httpd_port_json(port):
    return {"key": "httpd_port", "value": str(port)}

def __set_httpd_port_setting(conf, host, port):
    setting = conf.settings()._new_resource(__get_httpd_port_json(port))
    setting.create()
    __test_web_server(host, port)

def __update_httpd_port_setting(conf, host, port):
    setting = conf.settings().get_resource("httpd_port")
    setting.set_value(str(port))
    setting.commit()
    __test_web_server(host, port)

def __unset_httpd_port_setting(conf, host, port):
    setting = conf.settings().get_resource("httpd_port")
    setting.delete()
    __test_web_server(host, port)

def __set_httpd_port_setting_at_app(host, port):
    setting = host.application_settings(defs.global_vars.app_name)._new_resource(__get_httpd_port_json(port))
    setting.create()
    __test_web_server(host, port)

def __unset_httpd_port_setting_at_app(host, port):
    setting = host.application_settings(defs.global_vars.app_name).get_resource("httpd_port")
    setting.delete()
    __test_web_server(host, port)

def __test_web_server(host, port):
    while len(host.get_changes()) > 0:
        time.sleep(3)
    try:
        urllib2.urlopen("http://" + host.get_instance().get_ip() + ":" + str(port))
    except urllib2.HTTPError, e:
        if e.code != 403:
            raise Exception("Unexpected HTTP error: " + str(e.code))

def do_demo():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi(setup.global_vars.comodit_url, setup.global_vars.comodit_user, setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    print "Installing web server..."
    context = ApplicationContext()
    context.set_application(defs.global_vars.app_name)
    host.install_application(context)
    while len(host.get_changes()) > 0:
        time.sleep(3)

    print "Setting httpd_port at organization level..."
    __set_httpd_port_setting(org, host, 80)

    print "Setting httpd_port at environment level..."
    __set_httpd_port_setting(env, host, 88)

    print "Setting httpd_port at host level..."
    __set_httpd_port_setting(host, host, 8000)

    print "Setting httpd_port at application level..."
    __set_httpd_port_setting_at_app(host, 8888)

    print "Unsetting httpd_port at application level..."
    __unset_httpd_port_setting_at_app(host, 8000)

    print "Unsetting httpd_port at host level..."
    __unset_httpd_port_setting(host, host, 88)

    print "Unsetting httpd_port at environment level..."
    __unset_httpd_port_setting(env, host, 80)

    print "Unsetting httpd_port at organization level..."
    __unset_httpd_port_setting(org, host, 80)

    print "Setting httpd_port at host level..."
    __set_httpd_port_setting(host, host, 8000)

    print "Changing httpd_port at host level..."
    __update_httpd_port_setting(host, host, 80)

    print "Demo completed."


#==============================================================================
# Entry point
if __name__ == "__main__":
    setup.setup()
    defs.define()
    do_demo()
