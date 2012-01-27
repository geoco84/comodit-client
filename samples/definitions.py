import setup

#==============================================================================
# Definitions section

class Expendable(object):
    pass

global_vars = Expendable()

def define():
    # Define organization
    global_vars.org_name = "Guardis2"
    global_vars.org_description = "Guardis2's organization"

    # Define applications
    global_vars.guardis_repos_name = "GuardisRepos"
    global_vars.simple_web_page_name = "SimpleWebPage"
    global_vars.web_server_name = "WebServer"
    global_vars.app_names = [
                             global_vars.guardis_repos_name,
                             global_vars.simple_web_page_name,
                             global_vars.web_server_name
                             ]

    # Define platform
    global_vars.plat_name = "Local2"

    # Define distribution (kickstart template is in same folder)
    global_vars.dist_name = "co6"

    # Define environments
    global_vars.env_name = "Test2"
    global_vars.env_description = "Test environment 1 of Guardis2"

    # Define host
    global_vars.host_name = "test2"
    global_vars.host_description = "Single host of Test2 environment"
    global_vars.host_dist = global_vars.dist_name
    global_vars.host_plat = global_vars.plat_name
    global_vars.host_apps = [global_vars.guardis_repos_name]
    global_vars.host_settings = \
        [
            {"key":"vm_arch", "value": setup.global_vars.vm_arch},
            {"key":"vm_bridge", "value": setup.global_vars.vm_bridge},
            {"key":"vm_memory", "value":"512"},
            {"key":"vm_capacity", "value":"2048"},
            {"key":"vm_nvirtcpus", "value":"1"}
        ]

