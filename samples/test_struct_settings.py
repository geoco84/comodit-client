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

def setup(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    install_web_server(host)
    install_simple_web_page(host, [get_simple_setting_json("struct_setting", {"a": "a value", "b":"b value"})])

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    check_page_content(host, 80, "/index.html", "<p>Struct a: a value</p>")
    check_page_content(host, 80, "/index.html", "<p>Struct b: b value</p>")

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(test_setup.global_vars.org_name)
    env = org.environments().get_resource(test_setup.global_vars.env_name)
    host = env.hosts().get_resource(argv[0])

    uninstall_simple_web_page(host)
    uninstall_web_server(host)

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
