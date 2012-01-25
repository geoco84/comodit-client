import setup

#==============================================================================
# Definitions section

class Expendable(object):
    pass

global_vars = Expendable()

def define_web_server():
    name = "WebServer"
    global_vars.web_server_name = name

    desc = Expendable()
    global_vars.apps[name] = desc

    desc.name = name
    desc.description = "Apache web server"

    # Packages
    desc.packages = \
        [
            {"name": "httpd"},
            {"name": "mod_ssl"}
        ]

    # Files
    desc.files = []

    # 'httpd.conf' file
    desc.files.append(Expendable())
    desc.files[0].meta = {
                "owner": "root",
                "group": "root",
                "mode": "644",
                "name": "httpd.conf",
                "path": "/etc/httpd/conf/httpd.conf",
                "template": {
                    "name": "httpd.conf"
                }
            }
    desc.files[0].content = "httpd.conf"

    # Services
    desc.services = \
        [
            {
                "name": "httpd",
                "enabled": "true"
            }
        ]

    # Handlers
    desc.handlers = \
        [
            {
                "do": [
                    {
                        "action": "update",
                        "resource": "file://" + desc.files[0].meta["name"]
                    },
                    {
                        "action": "restart",
                        "resource": "service://" + desc.services[0]["name"]
                    }
                ],
                "on": [
                    "httpd_port"
                ]
            }
        ]

    # Parameters
    desc.parameters = \
        [
            {
                "description": "The httpd port",
                "key": "httpd_port",
                "name": "Httpd Port",
                "value": "80"
            }
        ]

def define_simple_web_page():
    name = "SimpleWebPage"
    global_vars.simple_web_page_name = name

    desc = Expendable()
    global_vars.apps[name] = desc

    desc.name = name
    desc.description = "A simple web page"

    # Packages
    desc.packages = []

    # Files
    desc.files = []

    # 'index.html' file
    desc.files.append(Expendable())
    desc.files[0].meta = {
                "owner": "root",
                "group": "root",
                "mode": "644",
                "name": "index.html",
                "path": "/var/www/html/index.html",
                "template": {
                    "name": "index.html"
                }
            }
    desc.files[0].content = "index.html"

    # Services
    desc.services = []

    # Handlers
    desc.handlers = [
            {
                "do": [
                    {
                        "action": "update",
                        "resource": "file://" + desc.files[0].meta["name"]
                    }
                ],
                "on": [
                    "simple_web_page", "list_setting", "struct_setting"
                ]
            }
        ]

    # Parameters
    desc.parameters = \
        [
            {
                "description": "A parameter whose value is displayed",
                "key": "simple_web_page",
                "name": "Simple web page's simple parameter",
                "value": "hello"
            },
            {
                "description": "A parameter whose value is displayed",
                "key": "list_setting",
                "name": "Simple web page's list parameter",
                "value": ["one", "two", "three"]
            },
            {
                "description": "A parameter whose value is displayed",
                "key": "struct_setting",
                "name": "Simple web page's struct parameter",
                "value": {"a": "a value", "b": "b value"}
            }
        ]

def define_guardis_repositories():
    name = "GuardisRepos"
    global_vars.guardis_repos_name = name

    desc = Expendable()
    global_vars.apps[name] = desc

    desc.name = name
    desc.description = "Guardis repositories"

    # Packages
    desc.packages = []

    # Files
    desc.files = []

    # 'CentOS-Base.repo' file
    desc.files.append(Expendable())
    desc.files[len(desc.files) - 1].meta = {
                "owner": "root",
                "group": "root",
                "mode": "644",
                "name": "CentOS-Base.repo",
                "path": "/etc/yum.repos.d/CentOS-Base.repo",
                "template": {
                    "name": "CentOS-Base.repo"
                }
            }
    desc.files[len(desc.files) - 1].content = "CentOS-Base.repo"

    # 'comodit.repo' file
    desc.files.append(Expendable())
    desc.files[len(desc.files) - 1].meta = {
                "owner": "root",
                "group": "root",
                "mode": "644",
                "name": "comodit.repo",
                "path": "/etc/yum.repos.d/comodit.repo",
                "template": {
                    "name": "comodit.repo"
                }
            }
    desc.files[len(desc.files) - 1].content = "comodit.repo"

    # 'comodit-dev.repo' file
    desc.files.append(Expendable())
    desc.files[len(desc.files) - 1].meta = {
                "owner": "root",
                "group": "root",
                "mode": "644",
                "name": "comodit-dev.repo",
                "path": "/etc/yum.repos.d/comodit-dev.repo",
                "template": {
                    "name": "comodit-dev.repo"
                }
            }
    desc.files[len(desc.files) - 1].content = "comodit-dev.repo"

    # 'epel.repo' file
    desc.files.append(Expendable())
    desc.files[len(desc.files) - 1].meta = {
                "owner": "root",
                "group": "root",
                "mode": "644",
                "name": "epel.repo",
                "path": "/etc/yum.repos.d/epel.repo",
                "template": {
                    "name": "epel.repo"
                }
            }
    desc.files[len(desc.files) - 1].content = "epel.repo"

    # 'yum_clean.sh' file
    desc.files.append(Expendable())
    desc.files[len(desc.files) - 1].meta = {
                "owner": "root",
                "group": "root",
                "mode": "755",
                "name": "yum_clean.sh",
                "path": "/etc/yum.repos.d/yum_clean.sh",
                "template": {
                    "name": "yum_clean.sh"
                }
            }
    desc.files[len(desc.files) - 1].content = "yum_clean.sh"

    # Services
    desc.services = []

    # Handlers
    actions = []
    for file_desc in desc.files:
        actions.append({
                        "action": "update",
                        "resource": "file://" + file_desc.meta["name"]
                        })
    desc.handlers = [
            {
                "do": actions,
                "on": [
                    "zone", "vm_arch", "vm_base_arch"
                ]
            },
            {
                "do": [
                    {
                        "action": "execute",
                        "resource": "file://yum_clean.sh"
                    }
                ],
                "on": [
                    "_install"
                ]
            }
        ]

    # Parameters
    desc.parameters = \
        [
            {
                "description": "The geographical zone of the VM",
                "key": "zone",
                "name": "Zone",
                "value": setup.global_vars.zone
            },
            {
                "description": "The base arch of the VM",
                "key": "vm_base_arch",
                "name": "VmBaseArch",
                "value": setup.global_vars.vm_base_arch
            },
            {
                "description": "The arch of the VM",
                "key": "vm_arch",
                "name": "VmArch",
                "value": setup.global_vars.vm_arch
            },
            {
                "description": "Flag to enable comodit-dev repository",
                "key": "enable_trunk",
                "name": "Enable trunk",
                "value": "true"
            }
        ]

def define():
    # Define organization
    global_vars.org_name = "Guardis2"
    global_vars.org_description = "Guardis2's organization"

    # Define applications
    global_vars.apps = {}
    define_web_server()
    define_simple_web_page()
    define_guardis_repositories()

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

