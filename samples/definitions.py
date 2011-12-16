#==============================================================================
# Definitions section

# ComodIT server
comodit_url = "http://localhost:8000/api"
comodit_user = "admin"
comodit_pass = "secret"

# Define organization
org_name = "Guardis2"
org_description = "Guardis2's organization"

# Define application
app_name = "WebServer"
app_packages = ["httpd", "mod_ssl"]
app_description = "Apache web server"

app_file_name = "httpd.conf"
app_file_meta = {
            "owner": "root",
            "group": "root",
            "mode": "644",
            "name": app_file_name,
            "path": "/etc/httpd/conf/httpd.conf",
            "template": {
                "name":app_file_name,
                "parameters": [
                    {
                        "description": "The httpd port",
                        "key": "httpd_port",
                        "name": "Httpd Port",
                        "value": "80"
                    }
                ]
            }
        }
app_file_content = "httpd.conf"
app_files = [(app_file_meta, app_file_content)]

app_service_name = "httpd"
app_services = [{
            "name": app_service_name,
            "enabled": "true"
        }]

app_handlers = [
        {
            "do": [
                {
                    "action": "update",
                    "resource": "file://" + app_file_name
                },
                {
                    "action": "restart",
                    "resource": "service://" + app_service_name
                }
            ],
            "on": [
                "httpd_port"
            ]
        }
    ]

# Define platform
plat_name = "Local2"
plat_description = "Local QEMU"
plat_driver = "com.guardis.cortex.server.driver.LibvirtDriver"
plat_settings = [{"key":"libvirt.connectUrl",
"value":"qemu:///system"}]
plat_files = \
    [
        {
            "name":"libvirt.domain.fmt",
            "parameters":
                [
                    {"key": "_libvirt_uuid", "value":""},
                    {"key": "_name", "value":""},
                    {"key": "_kernel", "value":""},
                    {"key": "_initrd", "value":""},
                    {"key": "_kickstart", "value":""},
                    {"key": "_path", "value":""},
                    {"key": "vm_memory", "value":""},
                    {"key": "vm_nvirtcpus", "value":""},
                    {"key": "vm_arch", "value":""},
                    {"key": "vm_mac", "value":""}
                ]
        },
        {
            "name":"libvirt.disk.fmt",
            "parameters":
                [
                    {"key": "_uuid", "value":""},
                    {"key": "vm_capacity", "value":""}
                ]
        }
    ]
plat_files_content = \
    {
        "libvirt.domain.fmt": "libvirt.domain.fmt.nat",
        "libvirt.disk.fmt": "libvirt.disk.fmt"
    }

# Define distribution (kickstart template is in same folder)
dist_name = "co6i686"
dist_description = "CentOS 6 i686"
dist_kickstart = "kickstart"
dist_settings = \
    [
        {
            "key": "kernel_params",
            "value": "text ks=${_api}/organizations/${_org_name}/environments/${_env_name}/hosts/${_host_name}/distribution/files/" + dist_kickstart
        },
        {
            "key":"initrd_path",
            "value":"/var/lib/libvirt/boot/initrd.img.centos.6.i386"
        },
        {
            "key":"vmlinuz_path",
            "value":"/var/lib/libvirt/boot/vmlinuz.centos.6.i386"
        }
    ]
dist_files = \
    [
        {
            "name":dist_kickstart,
            "parameters":
                [
                    {"key": "zone", "value":"angleur"},
                    {"key": "vm_arch", "value":"i686"},
                    {"key": "vm_base_arch", "value":"i386"},
                    {"key": "enable_trunk", "value":"true"},
                    {"key": "ks_rootpw_one", "value":"secret"}
                ]
        }
    ]

dist_kickstart_content = "co6.ks"

# Define environments
env_name = "Test2"
env_description = "Test environment 1 of Guardis2"

# Define host
host_name = "test2"
host_description = "Single host of Test2 environment"
host_dist = dist_name
host_plat = plat_name
host_apps = [] # Application will be installed after provisioning
host_settings = [{"key":"vm_arch", "value":"i686"},
{"key":"vm_bridge", "value":"br0"},
{"key":"vm_memory", "value":"512"},
{"key":"vm_capacity", "value":"2048"},
{"key":"vm_nvirtcpus", "value":"1"}]

