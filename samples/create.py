# Setup Python path
import sys
sys.path.append("..")
import setup
import definitions as defs



#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.application import Package, ApplicationFile, Service, \
    Handler
from cortex_client.api.settings import Setting
from cortex_client.api.file import File
from cortex_client.api.parameters import Parameter

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
        org = org_coll.get_resource(defs.global_vars.org_name)
        print "Organization already exists"
    except ResourceNotFoundException:
        org = create_org(api)
        print "Organization is created"
    org.show()

    app_coll = org.applications()
    for (name, desc) in defs.global_vars.apps.iteritems():
        print "="*80
        print "Application"
        try:
            app = app_coll.get_resource(name)
            print "Application already exists"
        except ResourceNotFoundException:
            app = create_app(org, desc)
            print "Application is created"
        app.show()

    print "="*80
    print "Platform"
    plat_coll = org.platforms()
    try:
        plat = plat_coll.get_resource(defs.global_vars.plat_name)
        print "Platform already exists"
    except ResourceNotFoundException:
        plat = create_plat(org)
        print "Platform is created"

    plat.show()

    print "="*80
    print "Distribution"
    dist_coll = org.distributions()
    try:
        dist = dist_coll.get_resource(defs.global_vars.dist_name)
        print "Distribution already exists"
    except ResourceNotFoundException:
        dist = create_dist(org)
        print "Distribution is created"
    dist.show()

    print "="*80
    print "Environments"
    env_coll = org.environments()
    try:
        env = env_coll.get_resource(defs.global_vars.env_name)
        print "Environment " + defs.global_vars.env_name + " already exists"
    except ResourceNotFoundException:
        env = create_env(org)
        print "Environment " + defs.global_vars.env_name + " is created"
    env.show()

    print "="*80
    print "Host"
    host_coll = env.hosts()
    try:
        host = host_coll.get_resource(defs.global_vars.host_name)
        print "Host already exists"
    except ResourceNotFoundException:
        host = create_host(env)
        print "Host is created"
    host.show()

def create_app(org, desc):
    """
    Creates an application linked to given API api
    """
    app = org.new_application(desc.name)
    app.set_description(desc.description)

    for p in desc.packages:
        app.add_package(Package(p))

    for p in desc.parameters:
        app.add_parameter(Parameter(None, p))

    for f in desc.files:
        app.add_file(ApplicationFile(None, f.meta))

    for s in desc.services:
        app.add_service(Service(s))

    for h in desc.handlers:
        app.add_handler(Handler(h))

    app.create()

    # Upload file contents
    for f in desc.files:
        file_res = app.files().get_resource(f.meta["name"])
        file_res.set_content(f.content)

    return app

def create_plat(org):
    """
    Creates a platform linked to given API api
    """
    plat = org.new_platform(defs.global_vars.plat_name)
    plat.set_description(defs.global_vars.plat_description)
    plat.set_driver(defs.global_vars.plat_driver)

    for s in defs.global_vars.plat_settings:
        plat.add_setting(Setting(None, s))

    for p in defs.global_vars.plat_parameters:
        plat.add_parameter(Parameter(None, p))

    for f in defs.global_vars.plat_files:
        plat.add_file(File(None, f))

    plat.create()

    for f in plat.get_files():
        plat.set_file_content(f.get_name(), defs.global_vars.plat_files_content.get(f.get_name()))

    return plat

def create_dist(org):
    """
    Creates a distribution linked to given API api
    """
    dist = org.new_distribution(defs.global_vars.dist_name)
    dist.set_description(defs.global_vars.dist_description)

    for s in defs.global_vars.dist_settings:
        dist.add_setting(Setting(None, s))

    for p in defs.global_vars.dist_parameters:
        dist.add_parameter(Parameter(None, p))

    for f in defs.global_vars.dist_files:
        dist.add_file(File(None, f))

    dist.create()

    dist.set_file_content(defs.global_vars.dist_kickstart, defs.global_vars.dist_kickstart_content)

    return dist

def create_org(api):
    """
    Creates an organization linked to given API api
    """
    org = api.new_organization(defs.global_vars.org_name)
    org.set_description(defs.global_vars.org_description)
    org.create()
    return org

def create_env(org):
    """
    Creates an environment linked to given API api
    """
    env = org.new_environment(defs.global_vars.env_name)
    env.set_description(defs.global_vars.env_description)
    env.create()
    return env

def create_host(env):
    """
    Creates a host linked to given API api
    """
    host = env.new_host(defs.global_vars.host_name)
    host.set_description(defs.global_vars.host_description)

    host.set_platform(defs.global_vars.plat_name)
    host.set_distribution(defs.global_vars.dist_name)

    for app_name in defs.global_vars.host_apps:
        host.add_application(app_name)

    for setting in defs.global_vars.host_settings:
        host.add_setting(Setting(None, setting))

    host.create()
    return host


#==============================================================================
# Entry point
if __name__ == "__main__":
    setup.setup()
    setup.create_kickstart()
    defs.define()
    create_resources()
