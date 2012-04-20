import os

class Globals(object):
    pass

global_vars = Globals()

repos = {}

def setup():
    global repos

    # Default values
    global_vars.comodit_url = "http://comodit-0-10.angleur.guardis.be:8000/api"
    global_vars.comodit_user = "admin"
    global_vars.comodit_pass = "secret"
    global_vars.amqp_server = "comodit-0-10.angleur.guardis.be"
    global_vars.vm_arch = "x86_64"
    global_vars.vm_base_arch = "x86_64"
    global_vars.zone = "angleur"
    global_vars.vm_bridge = "br0"
    global_vars.libvirt_domain_file = "files/libvirt.domain.fmt.br"
    global_vars.initrd = "/var/lib/libvirt/boot/initrd.img"
    global_vars.vmlinuz = "/var/lib/libvirt/boot/vmlinuz"
    global_vars.libvirt_connect_url = "qemu+ssh://baobab6.bruxelles/system"

    global_vars.email_dests = ["me@organization.com"]
    global_vars.smtp_ssl = False
    global_vars.smtp_server = "localhost"
    global_vars.smtp_user = None
    global_vars.smtp_pass = None

    global_vars.prov_time_out = 1800 # 1/2 hour time-out on provisioning
    global_vars.change_time_out = 120 # 2 minutes time-out on changes

    # Default repos, see co6.ks.template
    repos = {"base_url" : "http://oak.${zone}.guardis.be/public/centos/6/os/${vm_base_arch}/",
             "updates" : "http://oak.${zone}.guardis.be/public/centos/6/updates/${vm_base_arch}/",
             "epel": "http://oak.${zone}.guardis.be/public/epel/6/${vm_base_arch}/",
             "comodit": "http://oak.${zone}.guardis.be/public/comodit/centos/6/${vm_arch}/",
             "synapse": "http://oak.${zone}.guardis.be/public/synapse/centos/6/${vm_arch}/",
             "comodit-dev": "http://oak.${zone}.guardis.be/private/comodit-testing/centos/6/${vm_arch}/",
             "synapse-dev": "http://oak.${zone}.guardis.be/private/synapse-testing/centos/6/${vm_arch}/"}

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
        if var.__dict__.has_key("email_dests"):
            global_vars.email_dests = var.__dict__["email_dests"]
        if var.__dict__.has_key("smtp_ssl"):
            global_vars.smtp_ssl = var.__dict__["smtp_ssl"]
        if var.__dict__.has_key("smtp_server"):
            global_vars.smtp_server = var.__dict__["smtp_server"]
        if var.__dict__.has_key("smtp_user"):
            global_vars.smtp_user = var.__dict__["smtp_user"]
        if var.__dict__.has_key("smtp_pass"):
            global_vars.smtp_pass = var.__dict__["smtp_pass"]

        if var.__dict__.has_key("repos"):
            if var.repos.has_key("base_url"):
                repos["base_url"] = var.repos["base_url"]
            if var.repos.has_key("updates"):
                repos["updates"] = var.repos["updates"]
            if var.repos.has_key("epel"):
                repos["epel"] = var.repos["epel"]
            if var.repos.has_key("comodit"):
                repos["comodit"] = var.repos["comodit"]
            if var.repos.has_key("synapse"):
                repos["synapse"] = var.repos["synapse"]
            if var.repos.has_key("comodit-dev"):
                repos["comodit-dev"] = var.repos["comodit-dev"]
            if var.repos.has_key("synapse-dev"):
                repos["synapse-dev"] = var.repos["synapse-dev"]

def create_kickstart():
    global repos

    # Generate kickstart
    with open("files/co6.ks.template", "r") as f:
        content = f.read()
        content = content.replace("##repos_base_url##", repos["base_url"])
        content = content.replace("##repos_updates##", repos["updates"])
        content = content.replace("##repos_epel##", repos["epel"])
        content = content.replace("##repos_comodit##", repos["comodit"])
        content = content.replace("##repos_synapse##", repos["synapse"])
        content = content.replace("##repos_comodit-dev##", repos["comodit-dev"])
        content = content.replace("##repos_synapse-dev##", repos["synapse-dev"])

        with open("files/co6.ks", "w") as g:
            g.write(content)

def create_repo_files():
    global repos

    files = ["files/CentOS-Base.repo.template",
             "files/comodit.repo.template",
             "files/synapse.repo.template",
             "files/comodit-dev.repo.template",
             "files/synapse-dev.repo.template",
             "files/epel.repo.template"]

    for name in files:
        repo_name = name[:-9]
        with open(name, "r") as f:
            content = f.read()
            content = content.replace("##repos_base_url##", repos["base_url"])
            content = content.replace("##repos_updates##", repos["updates"])
            content = content.replace("##repos_epel##", repos["epel"])
            content = content.replace("##repos_comodit##", repos["comodit"])
            content = content.replace("##repos_synapse##", repos["synapse"])
            content = content.replace("##repos_comodit-dev##", repos["comodit-dev"])
            content = content.replace("##repos_synapse-dev##", repos["synapse-dev"])

            with open(repo_name, "w") as g:
                g.write(content)

def create_domain_file():
    domain = global_vars.libvirt_domain_file
    with open(domain, "r") as model:
        with open("files/libvirt.domain.fmt", "w") as output:
            output.write(model.read())

def _render_file(template_name, data):
    name = template_name[:-9]
    with open(template_name, "r") as f:
        content = f.read()

        for (key, value) in data.items():
            content = content.replace(key, value)

        with open(name, "w") as g:
            g.write(content)

def create_guardis_repositories_json():
    replacements = {"##zone##": global_vars.zone,
                    "##base_arch##": global_vars.vm_base_arch,
                    "##arch##": global_vars.vm_arch}
    _render_file("apps/GuardisRepos.json.template", replacements)

def create_dist_json():
    replacements = {"##arch##": global_vars.vm_arch,
                    "##base_arch##": global_vars.vm_base_arch,
                    "##amqp_server##": global_vars.amqp_server,
                    "##init_rd##": global_vars.initrd,
                    "##vmlinuz##": global_vars.vmlinuz,
                    "##zone##": global_vars.zone}
    _render_file("dists/co6-Local.json.template", replacements)
    _render_file("dists/co6-Hyp3.json.template", replacements)
    _render_file("dists/co6-VMWare.json.template", replacements)
    _render_file("dists/co6-CloudStack.json.template", replacements)

def create_files():
    create_kickstart()
    create_repo_files()
    create_domain_file()
    create_guardis_repositories_json()
    create_dist_json()

def delete_files():
    files = ["files/co6.ks",
             "files/libvirt.domain.fmt",
             "apps/GuardisRepos.json",
             "dists/co6.json"
             ]

    for f in files:
        try:
            os.remove(f)
        except:
            pass

if __name__ == "__main__":
    setup()
    create_files()

