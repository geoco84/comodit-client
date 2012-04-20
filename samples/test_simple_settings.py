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

def __set_httpd_port_setting(conf, host, port, time_out = 0):
    add_simple_setting(conf, "httpd_port", str(port))
    test_web_server_default(host, port, time_out)

def __update_httpd_port_setting(conf, host, port, time_out = 0):
    update_to_simple_setting(conf, "httpd_port", str(port))
    test_web_server_default(host, port, time_out)

def __unset_httpd_port_setting(host, conf):
    try:
        delete_setting(conf, "httpd_port")
    except PythonApiException, e:
        print e.message

def __unset_httpd_port_setting_and_test(conf, host, port, time_out = 0):
    delete_setting(conf, "httpd_port")
    test_web_server_default(host, port, time_out)

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
    app = host.applications().get_resource(test_setup.global_vars.web_server_name)

    time_out = get_time_out(argv)

    print "Setting httpd_port at organization level..."
    __set_httpd_port_setting(org, host, 80, time_out)

    print "Setting httpd_port at environment level..."
    __set_httpd_port_setting(env, host, 88, time_out)

    print "Setting httpd_port at host level..."
    __set_httpd_port_setting(host, host, 8000, time_out)

    print "Setting httpd_port at application level..."
    __set_httpd_port_setting(app, host, 8888, time_out)

    print "Unsetting httpd_port at application level..."
    __unset_httpd_port_setting_and_test(app, host, 8000, time_out)

    print "Unsetting httpd_port at host level..."
    __unset_httpd_port_setting_and_test(host, host, 88, time_out)

    print "Unsetting httpd_port at environment level..."
    __unset_httpd_port_setting_and_test(env, host, 80, time_out)

    print "Unsetting httpd_port at organization level..."
    __unset_httpd_port_setting_and_test(org, host, 80, time_out)

    print "Setting httpd_port at host level..."
    __set_httpd_port_setting(host, host, 8000, time_out)

    print "Changing httpd_port at host level..."
    __update_httpd_port_setting(host, host, 80, time_out)

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    uninstall_web_server(host, time_out)

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
