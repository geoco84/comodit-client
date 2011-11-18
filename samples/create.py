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
    api = CortexApi("http://localhost:8000/api", "admin", "secret")


    ##################################################################
    # Create entities (if they do not already exist) described above #
    ##################################################################

    print "="*80
    print "Application"
    app_coll = api.get_application_collection()
    try:
        app = app_coll.get_resource_from_path(app_name)
        print "Application already exists"
    except ResourceNotFoundException:
        app = create_app(api)
        print "Application is created"
    app.show()

    print "="*80
    print "Platform"
    plat_coll = api.get_platform_collection()
    try:
        plat = plat_coll.get_resource_from_path(plat_name)
        print "Platform already exists"
    except ResourceNotFoundException:
        plat = create_plat(api)
        print "Platform is created"
    plat.show()

    print "="*80
    print "Distribution"
    dist_coll = api.get_distribution_collection()
    try:
        dist = dist_coll.get_resource_from_path(dist_name)
        print "Distribution already exists"
    except ResourceNotFoundException:
        dist = create_dist(api)
        print "Distribution is created"
    dist.show()

    print "="*80
    print "Organization"
    org_coll = api.get_organization_collection()
    try:
        org = org_coll.get_resource_from_path(org_name)
        print "Organization already exists"
    except ResourceNotFoundException:
        org = create_org(api)
        print "Organization is created"
    org.show()

    print "="*80
    print "Environments"
    env_coll = api.get_environment_collection()
    envs = []
    for env_desc in org_envs:
        env_name = env_desc["name"]
        try:
            env = env_coll.get_resource_from_path(org_name + "/" + env_name)
            print "Environment " + env_name + " already exists"
        except ResourceNotFoundException:
            env = create_env(api, env_desc, org)
            print "Environment " + env_name + " is created"
        envs.append(env)
        env.show()

    print "="*80
    print "Host"
    host_coll = api.get_host_collection()
    try:
        host = host_coll.get_resource_from_path(host_env + "/" + host_name)
        print "Host already exists"
    except ResourceNotFoundException:
        host = create_host(api, host_env)
        print "Host is created"
    host.show()

def create_app(api):
    """
    Creates an application linked to given API api
    """
    app = api.new_application()
    app.set_name(app_name)
    app.set_description(app_description)

    for p in app_packages:
        app_pck = Package()
        app_pck.set_name(p)
        app.add_package(app_pck)

    app.create()
    return app

def create_plat(api):
    """
    Creates a platform linked to given API api
    """
    plat = api.new_platform()
    plat.set_name(plat_name)
    plat.set_description(plat_description)
    plat.set_driver(plat_driver)

    for s in plat_settings:
        plat.add_setting(Setting(s))

    plat.create()
    return plat

def create_dist(api):
    """
    Creates a distribution linked to given API api
    """
    dist = api.new_distribution()
    dist.set_name(dist_name)
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
    org = api.new_organization()
    org.set_name(org_name)
    org.set_description(org_description)
    org.create()
    return org

def create_env(api, env_desc, org):
    """
    Creates an environment linked to given API api
    """
    env = api.new_environment()
    env.set_name(env_desc["name"])
    env.set_description(env_desc["description"])
    env.set_organization(org.get_uuid())
    env.create()
    return env

def create_host(api, env_path):
    """
    Creates a host linked to given API api
    """
    host = api.new_host()
    host.set_name(host_name)
    host.set_description(host_description)

    env = api.get_environment_collection().get_resource_from_path(env_path)
    host.set_environment(env.get_uuid())

    plat = api.get_platform_collection().get_resource_from_path(host_plat)
    host.set_platform(plat.get_uuid())

    dist = api.get_distribution_collection().get_resource_from_path(host_dist)
    host.set_distribution(dist.get_uuid())

    for app_name in host_apps:
        app = api.get_application_collection().get_resource_from_path(app_name)
        host.add_application(app.get_uuid())

    for setting in host_settings:
        host.add_setting(Setting(setting))

    host.create()
    return host


#==============================================================================
# Entry point
if __name__ == "__main__":
    create_resources()
