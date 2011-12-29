# Setup Python path
import sys, setup
import definitions as defs
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.application import Package, ApplicationFile, Service, \
    Handler
from cortex_client.api.settings import Setting
from cortex_client.api.file import File, Parameter

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

    print "="*80
    print "Application"
    app_coll = org.applications()
    try:
        app = app_coll.get_resource(defs.global_vars.app_name)
        print "Application already exists"
    except ResourceNotFoundException:
        app = create_app(org)
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

def create_app(org):
    """
    Creates an application linked to given API api
    """
    app = org.new_application(defs.global_vars.app_name)
    app.set_description(defs.global_vars.app_description)

    for p in defs.global_vars.app_packages:
        app_pck = Package()
        app_pck.set_name(p)
        app.add_package(app_pck)

    for p in defs.global_vars.app_parameters:
        app.add_parameter(Parameter(p))

    for f in defs.global_vars.app_files:
        app.add_file(ApplicationFile(f[0]))

    for s in defs.global_vars.app_services:
        app.add_service(Service(s))

    for h in defs.global_vars.app_handlers:
        app.add_handler(Handler(h))

    app.create()

    # Upload file contents
    for f in defs.global_vars.app_files:
        app.set_file_content(f[0].get("name"), f[1])

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
        plat.add_parameter(Parameter(p))

    for f in defs.global_vars.plat_files:
        plat.add_file(File(f))

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
        dist.add_parameter(Parameter(p))

    for f in defs.global_vars.dist_files:
        dist.add_file(File(f))

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
