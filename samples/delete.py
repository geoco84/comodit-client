# Setup Python path
import sys
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi

from definitions import *


#==============================================================================
# Script

def delete_resources():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi("http://localhost:8000/api", "admin", "secret")

    app_coll = api.get_application_collection()
    app = app_coll.get_resource_from_path(app_name)

    plat_coll = api.get_platform_collection()
    plat = plat_coll.get_resource_from_path(plat_name)

    dist_coll = api.get_distribution_collection()
    dist = dist_coll.get_resource_from_path(dist_name)

    org_coll = api.get_organization_collection()
    org = org_coll.get_resource_from_path(org_name)

    env_coll = api.get_environment_collection()
    envs = []
    for env_desc in org_envs:
        env_name = env_desc["name"]
        env = env_coll.get_resource_from_path(org_name + "/" + env_name)
        envs.append(env)

    host_coll = api.get_host_collection()
    host = host_coll.get_resource_from_path(host_env + "/" + host_name)

    ###################
    # Delete entities #
    ###################

    try:
        host.poweroff()
    except:
        pass

    print "="*80
    print "Delete host (and VM)"
    try:
        host.delete(delete_vm = True)
    except Exception, e:
        print e.message

    print "="*80
    print "Delete application"
    try:
        app.delete()
    except Exception, e:
        print e.message

    print "="*80
    print "Delete platform"
    try:
        plat.delete()
    except Exception, e:
        print e.message

    print "="*80
    print "Delete distribution"
    try:
        dist.delete()
    except Exception, e:
        print e.message

    print "="*80
    print "Delete environments"
    for e in envs:
        try:
            e.delete()
        except Exception, e:
            print e.message

    print "="*80
    print "Delete organization"
    try:
        org.delete()
    except Exception, e:
        print e.message


#==============================================================================
# Entry point
if __name__ == "__main__":
    delete_resources()
