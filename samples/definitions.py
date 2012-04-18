import setup

#==============================================================================
# Definitions section

class Expendable(object):
    pass

global_vars = Expendable()

def get_host_name(plat_name):
    return "test-host-on-" + plat_name

def get_dist_name(plat_name):
    return "co6-" + plat_name

def define():
    # Define organization
    global_vars.org_name = "Guardis Test"
    global_vars.org_description = "Test Guardis Organization"

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
    global_vars.plat_names = ["Local", "Hyp3", "VMWare"]

    # Define distribution (kickstart template is in same folder)
    global_vars.dist_names = []
    for plat_name in global_vars.plat_names:
        global_vars.dist_names.append("co6-" + plat_name)

    # Define environments
    global_vars.env_name = "Test Environment"
    global_vars.env_description = "Test environment of test organization"

    # Define host
    global_vars.host_name = "test2"
    global_vars.host_description = "Single host of Test2 environment"
    global_vars.host_dist = global_vars.dist_names[0]
    global_vars.host_plat = global_vars.plat_names[0]
    global_vars.host_apps = [global_vars.guardis_repos_name]
    global_vars.host_settings = []

    # Define platform settings
    global_vars.plat_settings = {}
    global_vars.plat_settings["Local"] = \
        [
            {"key":"vm_memory", "value":"512"},
            {"key":"vm_capacity", "value":"2048"},
            {"key":"vm_nvirtcpus", "value":"1"}
        ]
    global_vars.plat_settings["Hyp3"] = \
        [
            {"key":"vm_memory", "value":"512"},
            {"key":"vm_capacity", "value":"2048"},
            {"key":"vm_nvirtcpus", "value":"1"}
        ]
    global_vars.plat_settings["VMWare"] = \
        [
            {"key":"vm_memory", "value":"512"},
            {"key":"vm_capacity", "value":"2048"},
            {"key":"vm_nvirtcpus", "value":"1"}
        ]
