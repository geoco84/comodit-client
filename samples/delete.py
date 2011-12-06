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
    api = CortexApi(comodit_url, comodit_user, comodit_pass)

    org_coll = api.organizations()
    try:
        org = org_coll.get_resource(org_name)
    except:
        print "Organization does not exist"

    app_coll = org.applications()
    try:
        app = app_coll.get_resource(app_name)
    except:
        print "Application does not exist"

    plat_coll = org.platforms()
    try:
        plat = plat_coll.get_resource(plat_name)
    except:
        print "Platform does not exist"

    dist_coll = org.distributions()
    try:
        dist = dist_coll.get_resource(dist_name)
    except:
        print "Distribution does not exist"

    env_coll = org.environments()
    try:
        env = env_coll.get_resource(env_name)
    except:
        print "Environment does not exist"

    host_coll = env.hosts()
    try:
        host = host_coll.get_resource(host_name)
    except:
        print "Host does not exist"

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
    try:
        env.delete()
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
