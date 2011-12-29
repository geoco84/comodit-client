import setup

#==============================================================================
# Definitions section

class Globals(object):
    pass

global_vars = Globals()

def define():
    # Define organization
    global_vars.org_name = "Guardis2"
    global_vars.org_description = "Guardis2's organization"

    # Define application
    global_vars.app_name = "WebServer"
    global_vars.app_packages = ["httpd", "mod_ssl"]
    global_vars.app_description = "Apache web server"

    global_vars.app_file_name = "httpd.conf"
    global_vars.app_file_meta = {
                "owner": "root",
                "group": "root",
                "mode": "644",
                "name": global_vars.app_file_name,
                "path": "/etc/httpd/conf/httpd.conf",
                "template": {
                    "name": global_vars.app_file_name
                }
            }
    global_vars.app_file_content = "httpd.conf"
    global_vars.app_files = [(global_vars.app_file_meta, global_vars.app_file_content)]
    global_vars.app_parameters = \
        [
            {
                "description": "The httpd port",
                "key": "httpd_port",
                "name": "Httpd Port",
                "value": "80"
            }
        ]

    global_vars.app_service_name = "httpd"
    global_vars.app_services = [{
                "name": global_vars.app_service_name,
                "enabled": "true"
            }]

    global_vars.app_handlers = [
            {
                "do": [
                    {
                        "action": "update",
                        "resource": "file://" + global_vars.app_file_name
                    },
                    {
                        "action": "restart",
                        "resource": "service://" + global_vars.app_service_name
                    }
                ],
                "on": [
                    "httpd_port"
                ]
            }
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
            {"key": "_libvirt_uuid", "value":""},
            {"key": "_name", "value":""},
            {"key": "_kernel", "value":""},
            {"key": "_initrd", "value":""},
            {"key": "_kickstart", "value":""},
            {"key": "_path", "value":""},
            {"key": "_uuid", "value":""},
            {"key": "vm_memory", "value":""},
            {"key": "vm_nvirtcpus", "value":""},
            {"key": "vm_arch", "value":""},
            {"key": "vm_mac", "value":""},
            {"key": "vm_capacity", "value":""}
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
            {"key": "zone", "value": setup.global_vars.zone},
            {"key": "vm_arch", "value": setup.global_vars.vm_arch},
            {"key": "vm_base_arch", "value": setup.global_vars.vm_base_arch},
            {"key": "enable_trunk", "value": "true"},
            {"key": "ks_rootpw_one", "value": "secret"},
            {"key": "amqp_server", "value": setup.global_vars.amqp_server}
        ]

    # Define environments
    global_vars.env_name = "Test2"
    global_vars.env_description = "Test environment 1 of Guardis2"

    # Define host
    global_vars.host_name = "test2"
    global_vars.host_description = "Single host of Test2 environment"
    global_vars.host_dist = global_vars.dist_name
    global_vars.host_plat = global_vars.plat_name
    global_vars.host_apps = [] # Application will be installed after provisioning
    global_vars.host_settings = \
        [
            {"key":"vm_arch", "value": setup.global_vars.vm_arch},
            {"key":"vm_bridge", "value": setup.global_vars.vm_bridge},
            {"key":"vm_memory", "value":"512"},
            {"key":"vm_capacity", "value":"2048"},
            {"key":"vm_nvirtcpus", "value":"1"}
        ]

