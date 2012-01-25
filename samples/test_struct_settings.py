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

def setup():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    install_web_server(host)
    install_simple_web_page(host, [get_simple_setting_json("struct_setting", {"a": "a value", "b":"b value"})])

def run():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    check_page_content(host, 80, "/index.html", "<p>Struct a: a value</p>")
    check_page_content(host, 80, "/index.html", "<p>Struct b: b value</p>")

def tear_down():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)
    env = org.environments().get_resource(defs.global_vars.env_name)
    host = env.hosts().get_resource(defs.global_vars.host_name)

    uninstall_simple_web_page(host)
    uninstall_web_server(host)

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
