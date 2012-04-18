# Setup Python path
import sys, setup
import definitions as defs
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi
from cortex_client.api.collection import ResourceNotFoundException


#==============================================================================
# Script

def delete_resources():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi(setup.global_vars.comodit_url, setup.global_vars.comodit_user, setup.global_vars.comodit_pass)

    org_coll = api.organizations()
    try:
        org = org_coll.get_resource(defs.global_vars.org_name)

        app_coll = org.applications()
        apps = []
        for name in defs.global_vars.app_names:
            try:
                apps.append(app_coll.get_resource(name))
            except ResourceNotFoundException:
                print "Application", name, "does not exist"

        plat_coll = org.platforms()
        plats = []
        for name in defs.global_vars.plat_names:
            try:
                plats.append(plat_coll.get_resource(name))
            except ResourceNotFoundException:
                print "Platform does not exist"

        dist_coll = org.distributions()
        dists = []
        for name in defs.global_vars.dist_names:
            try:
                dists.append(dist_coll.get_resource(name))
            except ResourceNotFoundException:
                print "Distribution does not exist"

        env_coll = org.environments()
        try:
            env = env_coll.get_resource(defs.global_vars.env_name)

            host_coll = env.hosts()
            try:
                host = host_coll.get_resource(defs.global_vars.host_name)
            except ResourceNotFoundException:
                print "Host does not exist"
        except ResourceNotFoundException:
            print "Environment does not exist"
    except ResourceNotFoundException:
        print "Organization does not exist"


    ###################
    # Delete entities #
    ###################

    print "="*80
    print "Delete host"
    try:
        host.delete()
    except Exception, e:
        print e.message

    print "="*80
    print "Delete applications"
    try:
        for app in apps:
            try:
                app.delete()
            except Exception, e:
                print e.message
    except Exception, e:
        print e.message

    print "="*80
    print "Delete platform"
    try:
        for plat in plats:
            try:
                plat.delete()
            except Exception, e:
                print e.message
    except Exception, e:
        print e.message

    print "="*80
    print "Delete distribution"
    try:
        for dist in dists:
            try:
                dist.delete()
            except Exception, e:
                print e.message
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


def delete_host_instance():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi(setup.global_vars.comodit_url, setup.global_vars.comodit_user, setup.global_vars.comodit_pass)

    org_coll = api.organizations()
    try:
        org = org_coll.get_resource(defs.global_vars.org_name)
        env_coll = org.environments()
        try:
            env = env_coll.get_resource(defs.global_vars.env_name)

            host_coll = env.hosts()
            try:
                host = host_coll.get_resource(defs.global_vars.host_name)
            except ResourceNotFoundException:
                print "Host does not exist"

            try:
                host.instance().get_single_resource().poweroff()
            except:
                pass

            print "="*80
            print "Delete host instance"
            try:
                host.instance().get_single_resource().delete()
            except Exception, e:
                print e.message
        except ResourceNotFoundException:
            print "Environment does not exist"
    except ResourceNotFoundException:
        print "Organization does not exist"


#==============================================================================
# Entry point
if __name__ == "__main__":
    setup.setup()
    defs.define()
    delete_host_instance()
    delete_resources()
