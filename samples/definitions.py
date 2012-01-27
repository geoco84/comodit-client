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
    global_vars.plat_description = "Local QEMU"
    global_vars.plat_driver = "com.guardis.cortex.server.driver.LibvirtDriver"
    global_vars.plat_settings = \
        [
            {"key": "libvirt.connectUrl", "value": setup.global_vars.libvirt_connect_url}
        ]
    global_vars.plat_files = \
        [
            {
                "name":"libvirt.domain.fmt"
            },
            {
                "name":"libvirt.disk.fmt"
            }
        ]
    global_vars.plat_files_content = \
        {
            "libvirt.domain.fmt": setup.global_vars.libvirt_domain_file,
            "libvirt.disk.fmt": "libvirt.disk.fmt"
        }
    global_vars.plat_parameters = \
        [
            {"key": "vm_memory", "value":"", "name":"Memory"},
            {"key": "vm_nvirtcpus", "value":"", "name":"VirtCpus"},
            {"key": "vm_arch", "value":"", "name":"Architecture"},
            {"key": "vm_mac", "value":"", "name":"MacAddress"},
            {"key": "vm_capacity", "value":"", "name":"Capacity"}
        ]

    # Define distribution (kickstart template is in same folder)
    global_vars.dist_name = "co6i686"
    global_vars.dist_description = "CentOS 6 i686"
    global_vars.dist_kickstart = "kickstart"
    global_vars.dist_settings = \
        [
            {
                "key": "kernel_params",
                "value": "text ks=${_api}/organizations/${_org_name?url}/environments/${_env_name?url}/hosts/${_host_name?url}/distribution/files/" + global_vars.dist_kickstart
            },
            {
                "key":"initrd_path",
                "value":setup.global_vars.initrd
            },
            {
                "key":"vmlinuz_path",
                "value":setup.global_vars.vmlinuz
            }
        ]
    global_vars.dist_files = \
        [
            {
                "name": global_vars.dist_kickstart
            }
        ]
    global_vars.dist_kickstart_content = "co6.ks"
    global_vars.dist_parameters = \
        [
            {"key": "zone", "value": setup.global_vars.zone, "name": "Zone"},
            {"key": "vm_arch", "value": setup.global_vars.vm_arch, "name": "Architecture"},
            {"key": "vm_base_arch", "value": setup.global_vars.vm_base_arch, "name": "Base architecture"},
            {"key": "enable_trunk", "value": "true", "name": "Enable trunk"},
            {"key": "ks_rootpw_one", "value": "secret", "name": "Root password"},
            {"key": "amqp_server", "value": setup.global_vars.amqp_server, "name": "AMQP server"}
        ]

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

