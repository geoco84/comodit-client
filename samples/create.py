# Setup Python path
import sys
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.application import Package
from cortex_client.api.host import Setting
from cortex_client.api.file import Parameter, File

from definitions import *

#==============================================================================
# Script

def create_resources():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi(comodit_url, comodit_user, comodit_pass)


    ##################################################
    # Create entities (if they do not already exist) #
    ##################################################

    print "="*80
    print "Organization"
    org_coll = api.organizations()
    try:
        org = org_coll.get_resource(org_name)
        print "Organization already exists"
    except ResourceNotFoundException:
        org = create_org(api)
        print "Organization is created"
    org.show()

    print "="*80
    print "Application"
    app_coll = org.applications()
    try:
        app = app_coll.get_resource(app_name)
        print "Application already exists"
    except ResourceNotFoundException:
        app = create_app(org)
        print "Application is created"
    app.show()

    print "="*80
    print "Platform"
    plat_coll = org.platforms()
    try:
        plat = plat_coll.get_resource(plat_name)
        print "Platform already exists"
    except ResourceNotFoundException:
        plat = create_plat(org)
        print "Platform is created"

    plat.show()

    print "="*80
    print "Distribution"
    dist_coll = org.distributions()
    try:
        dist = dist_coll.get_resource(dist_name)
        print "Distribution already exists"
    except ResourceNotFoundException:
        dist = create_dist(org)
        print "Distribution is created"
    dist.show()

    print "="*80
    print "Environments"
    env_coll = org.environments()
    try:
        env = env_coll.get_resource(env_name)
        print "Environment " + env_name + " already exists"
    except ResourceNotFoundException:
        env = create_env(org)
        print "Environment " + env_name + " is created"
    env.show()

    print "="*80
    print "Host"
    host_coll = env.hosts()
    try:
        host = host_coll.get_resource(host_name)
        print "Host already exists"
    except ResourceNotFoundException:
        host = create_host(env)
        print "Host is created"
    host.show()

def create_app(org):
    """
    Creates an application linked to given API api
    """
    app = org.new_application(app_name)
    app.set_description(app_description)

    for p in app_packages:
        app_pck = Package()
        app_pck.set_name(p)
        app.add_package(app_pck)

    app.create()
    return app

def create_plat(org):
    """
    Creates a platform linked to given API api
    """
    plat = org.new_platform(plat_name)
    plat.set_description(plat_description)
    plat.set_driver(plat_driver)

    for s in plat_settings:
        plat.add_setting(Setting(s))

    plat.create()
    return plat

def create_dist(org):
    """
    Creates a distribution linked to given API api
    """
    dist = org.new_distribution(dist_name)
    dist.set_description(dist_description)
    dist.set_initrd(dist_initrd)
    dist.set_vmlinuz(dist_vmlinuz)

    # Create kickstart template
    kickstart_file = File()
    kickstart_file.set_name(dist_name + " kickstart")
    for p in dist_kickstart_params:
        kickstart_file.add_parameter(Parameter(p))

    dist.set_kickstart(kickstart_file)
    dist.create()

    dist.set_kickstart_content(dist_kickstart)

    return dist

def create_org(api):
    """
    Creates an organization linked to given API api
    """
    org = api.new_organization(org_name)
    org.set_description(org_description)
    org.create()
    return org

def create_env(org):
    """
    Creates an environment linked to given API api
    """
    env = org.new_environment(env_name)
    env.set_description(env_description)
    env.create()
    return env

def create_host(env):
    """
    Creates a host linked to given API api
    """
    host = env.new_host(host_name)
    host.set_description(host_description)

    host.set_platform(plat_name)
    host.set_distribution(dist_name)

    for app_name in host_apps:
        host.add_application(app_name)

    for setting in host_settings:
        host.add_setting(Setting(setting))

    host.create()
    return host


#==============================================================================
# Entry point
if __name__ == "__main__":
    create_resources()
