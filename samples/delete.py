# Setup Python path
import sys, setup
import definitions as defs
sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi


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
        try:
            app = app_coll.get_resource(defs.global_vars.app_name)
        except:
            print "Application does not exist"

        plat_coll = org.platforms()
        try:
            plat = plat_coll.get_resource(defs.global_vars.plat_name)
        except:
            print "Platform does not exist"

        dist_coll = org.distributions()
        try:
            dist = dist_coll.get_resource(defs.global_vars.dist_name)
        except:
            print "Distribution does not exist"

        env_coll = org.environments()
        try:
            env = env_coll.get_resource(defs.global_vars.env_name)

            host_coll = env.hosts()
            try:
                host = host_coll.get_resource(defs.global_vars.host_name)
            except:
                print "Host does not exist"
        except:
            print "Environment does not exist"
    except:
        print "Organization does not exist"


    ###################
    # Delete entities #
    ###################

    try:
        host.poweroff()
    except:
        pass

    print "="*80
    print "Delete host instance"
    try:
        host.deleteInstance()
    except Exception, e:
        print e.message

    print "="*80
    print "Delete host"
    try:
        host.delete()
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
    setup.setup()
    defs.define()
    delete_resources()
