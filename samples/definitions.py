#==============================================================================
# Definitions section

# Define organization
org_name = "Guardis2"
org_description = "Guardis2's organization"

# Define application
app_name = "htop2"
app_packages = ["htop"]
app_description = "Htop Application"

# Define platform
plat_name = "Local2"
plat_description = "Local QEMU"
plat_driver = "com.guardis.cortex.server.services.provisioning.LibvirtDriver"
plat_settings = [{"key":"libvirt.connectUrl",
"value":"qemu:///system"}]

# Define distribution (kickstart template is in same folder)
dist_name = "co6i686"
dist_description = "CentOS 6 i686"
dist_url = "http://oak.angleur.guardis.be/public/centos/6.0/os/i386/"
dist_initrd = "/var/lib/libvirt/boot/initrd.img.centos.6.i386"
dist_vmlinuz = "/var/lib/libvirt/boot/vmlinuz.centos.6.i386"

dist_kickstart = "co6.ks"
dist_kickstart_params = [{"key": "zone", "value":"angleur"},
{"key": "vm_arch", "value":"i686"},
{"key": "vm_base_arch", "value":"i386"},
{"key": "enable_trunk", "value":"true"},
{"key": "ks_rootpw_one", "value":"secret"}]

# Define environments
env_name = "Test2"
env_description = "Test environment 1 of Guardis2"

# Define host
host_name = "test2"
host_description = "Single host of Test2 environment"
host_env = "Guardis2/Test2"
host_dist = dist_name
host_plat = plat_name
host_apps = [app_name]
host_settings = [{"key":"vm_arch", "value":"i686"},
{"key":"vm_bridge", "value":"br0"},
{"key":"vm_memory", "value":"1024"},
{"key":"vm_capacity", "value":"3072"},
{"key":"vm_nvirtcpus", "value":"1"}]

