# Setup Python path
import sys, test_utils
import definitions as defs
import setup as test_setup
from test_webserver import install_web_server, uninstall_web_server
from test_simple_web_page import get_simple_setting_json, install_simple_web_page, check_page_content, uninstall_simple_web_page
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi


#==============================================================================
# Script

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
    install_simple_web_page(host, [get_simple_setting_json("struct_setting", {"a": "a value", "b":"b value"})], time_out)

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    check_page_content(host, 80, "/index.html", "<p>Struct a: a value</p>", time_out)
    check_page_content(host, 80, "/index.html", "<p>Struct b: b value</p>", time_out)

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    time_out = get_time_out(argv)

    uninstall_simple_web_page(host, time_out)
    uninstall_web_server(host, time_out)

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
