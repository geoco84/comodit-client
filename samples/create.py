# Setup Python path
import sys, json
sys.path.append("..")
import setup
import definitions as defs


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.settings import Setting

#==============================================================================
# Script

def create_resources():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi(setup.global_vars.comodit_url, setup.global_vars.comodit_user, setup.global_vars.comodit_pass)


    ##################################################
    # Create entities (if they do not already exist) #
    ##################################################

    print "="*80
    print "Organization"
    org_coll = api.organizations()
    try:
        org = org_coll.get_resource(setup.global_vars.org_name)
        print "Organization already exists"
    except ResourceNotFoundException:
        org = create_org(api)
        print "Organization is created"
    org.show()

    app_coll = org.applications()
    for name in setup.global_vars.app_names:
        print "="*80
        print "Application", name
        try:
            app = app_coll.get_resource(name)
            print "Application already exists"
        except ResourceNotFoundException:
            app = create_app(org, name)
            print "Application is created"
        app.show()

    plat_coll = org.platforms()
    for name in setup.global_vars.plat_names:
        print "="*80
        print "Platform", name
        try:
            plat = plat_coll.get_resource(name)
            print "Platform already exists"
        except ResourceNotFoundException:
            plat = create_plat(org, name)
            print "Platform is created"
        plat.show()

    dist_coll = org.distributions()
    for name in setup.global_vars.dist_names:
        print "="*80
        print "Distribution", name
        try:
            dist = dist_coll.get_resource(name)
            print "Distribution already exists"
        except ResourceNotFoundException:
            dist = create_dist(org, name)
            print "Distribution is created"
        dist.show()

    print "="*80
    print "Environments"
    env_coll = org.environments()
    try:
        env = env_coll.get_resource(setup.global_vars.env_name)
        print "Environment " + setup.global_vars.env_name + " already exists"
    except ResourceNotFoundException:
        env = create_env(org)
        print "Environment " + setup.global_vars.env_name + " is created"
    env.show()

    print "="*80
    print "Host"
    host_coll = env.hosts()
    for plat_name in setup.global_vars.plat_names:
        try:
            host = host_coll.get_resource(defs.get_host_name(plat_name))
            print "Host already exists"
        except ResourceNotFoundException:
            host = create_host(env, plat_name)
            print "Host is created"
        host.show()

def create_app(org, name):
    """
    Creates an application linked to given API api
    """
    app = org.new_application(name)
    app.load_json("apps/" + name + ".json")
    app.create()

    # Upload file contents
    for f in app.get_files():
        file_res = app.files().get_resource(f.get_name())
        file_res.set_content("files/" + f.get_name())

    return app

def create_plat(org, name):
    """
    Creates a platform linked to given API api
    """
    plat = org.new_platform(name)

    data = {}
    with open("plats/" + name + ".json", 'r') as f:
        data = json.load(f)
    files = data.pop("files", [])

    plat.set_json(data)

    plat.create(parameters = {"default": "true"})

    # Update files
    for f in files:
        print "Updating file", f
        plat.files().get_resource(f).set_content("files/" + f)

    return plat

def create_dist(org, name):
    """
    Creates a distribution linked to given API api
    """
    dist = org.new_distribution(name)
    dist.load_json("dists/" + name + ".json")

    dist.create()

    for f in dist.get_files():
        f.set_content("files/" + f.get_name())

    return dist

def create_org(api):
    """
    Creates an organization linked to given API api
    """
    org = api.new_organization(setup.global_vars.org_name)
    org.set_description(setup.global_vars.org_description)
    org.create()
    return org

def create_env(org):
    """
    Creates an environment linked to given API api
    """
    env = org.new_environment(setup.global_vars.env_name)
    env.set_description(setup.global_vars.env_description)
    env.create()
    return env

def create_host(env, plat_name):
    """
    Creates a host linked to given API api
    """
    dist_name = defs.get_dist_name(plat_name)
    host = env.new_host(defs.get_host_name(plat_name))
    host.set_description("Test host using distribution " + dist_name + " on platform " + plat_name)

    host.set_platform(plat_name)
    host.set_distribution(dist_name)
    host.add_application(setup.global_vars.guardis_repos_name)

    host.create()

    context = host.platform().get_single_resource()
    for setting in setup.global_vars.plat_settings[plat_name]:
        s = context.new_setting(setting["key"])
        s.set_value(setting["value"])
        s.create()

    return host


#==============================================================================
# Entry point
if __name__ == "__main__":
    setup.setup()
    setup.create_files()
    defs.define()
    create_resources()
