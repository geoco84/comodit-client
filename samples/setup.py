import os

class Globals(object):
    pass

global_vars = Globals()

repos = {}

def setup():
    global repos

    # Default values
    global_vars.comodit_url = "http://comodit-dev.angleur.guardis.be:8000/api"
    global_vars.comodit_user = "admin"
    global_vars.comodit_pass = "secret"
    global_vars.amqp_server = "comodit-dev.angleur.guardis.be"
    global_vars.vm_arch = "x86_64"
    global_vars.vm_base_arch = "x86_64"
    global_vars.zone = "angleur"
    global_vars.vm_bridge = "br0"
    global_vars.libvirt_domain_file = "libvirt.domain.fmt.br"
    global_vars.initrd = "/var/lib/libvirt/boot/initrd.img"
    global_vars.vmlinuz = "/var/lib/libvirt/boot/vmlinuz"
    global_vars.libvirt_connect_url = "qemu+ssh://baobab6.bruxelles/system"

    # Default repos, see co6.ks.template
    repos = {"base_url" : "http://oak.${zone}.guardis.be/public/centos/6/os/${vm_base_arch}/",
             "updates" : "http://oak.${zone}.angleur.guardis.be/public/centos/6/updates/${vm_base_arch}/",
             "epel": "http://oak.${zone}.angleur.guardis.be/public/epel/6/${vm_base_arch}/",
             "comodit": "http://devel.bruxelles.guardis.be/public/comodit/centos/6/${vm_arch}/",
             "comodit-dev": "http://devel.bruxelles.angleur.guardis.be/public/comodit-dev/centos/6/${vm_arch}/"}

    # Override default values with values from file 'var.py'
    if os.path.exists("var.py"):
        import var
        if var.__dict__.has_key("comodit_url"):
            global_vars.comodit_url = var.__dict__["comodit_url"]
        if var.__dict__.has_key("comodit_usbase_urler"):
            global_vars.comodit_user = var.__dict__["comodit_user"]
        if var.__dict__.has_key("comodit_pass"):
            global_vars.comodit_pass = var.__dict__["comodit_pass"]
        if var.__dict__.has_key("amqp_server"):
            global_vars.amqp_server = var.__dict__["amqp_server"]
        if var.__dict__.has_key("vm_arch"):
            global_vars.vm_arch = var.__dict__["vm_arch"]
        if var.__dict__.has_key("vm_base_arch"):
            global_vars.vm_base_arch = var.__dict__["vm_base_arch"]
        if var.__dict__.has_key("zone"):
            global_vars.zone = var.__dict__["zone"]
        if var.__dict__.has_key("vm_bridge"):
            global_vars.vm_bridge = var.__dict__["vm_bridge"]
        if var.__dict__.has_key("libvirt_domain_file"):
            global_vars.libvirt_domain_file = var.__dict__["libvirt_domain_file"]
        if var.__dict__.has_key("initrd"):
            global_vars.initrd = var.__dict__["initrd"]
        if var.__dict__.has_key("vmlinuz"):
            global_vars.vmlinuz = var.__dict__["vmlinuz"]
        if var.__dict__.has_key("libvirt_connect_url"):
            global_vars.libvirt_connect_url = var.__dict__["libvirt_connect_url"]

        if var.__dict__.has_key("repos"):
            if var.repos.has_key("base_url"):
                repos["base_url"] = var.repos["base_url"]
            if var.repos.has_key("updates"):
                repos["updates"] = var.repos["updates"]
            if var.repos.has_key("epel"):
                repos["epel"] = var.repos["epel"]
            if var.repos.has_key("comodit"):
                repos["comodit"] = var.repos["comodit"]
            if var.repos.has_key("comodit-dev"):
                repos["comodit-dev"] = var.repos["comodit-dev"]

def create_kickstart():
    global repos

    # Generate kickstart
    with open("co6.ks.template", "r") as f:
        content = f.read()
        content = content.replace("##repos_base_url##", repos["base_url"])
        content = content.replace("##repos_updates##", repos["updates"])
        content = content.replace("##repos_epel##", repos["epel"])
        content = content.replace("##repos_comodit##", repos["comodit"])
        content = content.replace("##repos_comodit-dev##", repos["comodit-dev"])

        with open("co6.ks", "w") as g:
            g.write(content)

if __name__ == "__main__":
    setup()
    create_kickstart()
