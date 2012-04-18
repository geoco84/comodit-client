# Setup Python path
import sys, test_utils
import definitions as defs
import setup as test_setup
from test_webserver import test_web_server_default, install_web_server, uninstall_web_server
from test_simple_web_page import get_simple_setting_json
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def add_simple_setting(conf, key, value):
    setting = conf.settings()._new_resource(get_simple_setting_json(key, value))
    setting.create()

def update_to_simple_setting(conf, key, value):
    setting = conf.settings().get_resource(key)
    setting.set_value(value)
    setting.commit()

def delete_setting(conf, key):
    setting = conf.settings().get_resource(key)
    setting.delete()

def __set_httpd_port_setting(conf, host, port):
    add_simple_setting(conf, "httpd_port", str(port))
    test_web_server_default(host, port)

def __update_httpd_port_setting(conf, host, port):
    update_to_simple_setting(conf, "httpd_port", str(port))
    test_web_server_default(host, port)

def __unset_httpd_port_setting(host, conf):
    try:
        delete_setting(conf, "httpd_port")
    except PythonApiException, e:
        print e.message

def __unset_httpd_port_setting_and_test(conf, host, port):
    delete_setting(conf, "httpd_port")
    test_web_server_default(host, port)

def setup(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    install_web_server(host)

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])
    app = host.applications().get_resource(test_setup.global_vars.web_server_name)

    print "Setting httpd_port at organization level..."
    __set_httpd_port_setting(org, host, 80)

    print "Setting httpd_port at environment level..."
    __set_httpd_port_setting(env, host, 88)

    print "Setting httpd_port at host level..."
    __set_httpd_port_setting(host, host, 8000)

    print "Setting httpd_port at application level..."
    __set_httpd_port_setting(app, host, 8888)

    print "Unsetting httpd_port at application level..."
    __unset_httpd_port_setting_and_test(app, host, 8000)

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

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    uninstall_web_server(host)

    print "Removing httpd_port from organization..."
    __unset_httpd_port_setting(host, org)

    print "Removing httpd_port from environment..."
    __unset_httpd_port_setting(host, env)

    print "Removing httpd_port from host..."
    __unset_httpd_port_setting(host, host)

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
