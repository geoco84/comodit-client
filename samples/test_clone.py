# Setup Python path
import sys, test_utils
import definitions as defs
import setup as test_setup

from definitions import global_vars as gvs

sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi


#==============================================================================
# Script

def setup():
    pass

def run():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)

    print "Clone application"
    app = org.applications().get_resource(gvs.web_server_name)
    app.clone("newName")

    print "Clone distribution"
    dist = org.distributions().get_resource(gvs.dist_name)
    dist.clone("newName")

    print "Clone platform"
    plat = org.platforms().get_resource(gvs.plat_name)
    plat.clone("newName")

    print "Clone environment"
    env = org.environments().get_resource(gvs.env_name)
    env.clone("newName")

    print "Clone host"
    host = env.hosts().get_resource(gvs.host_name)
    host.clone()

def tear_down():
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(defs.global_vars.org_name)

    print "Removing application clone"
    try:
        app = org.applications().get_resource("newName")
        app.delete()
    except:
        pass

    print "Removing distribution clone"
    try:
        dist = org.distributions().get_resource("newName")
        dist.delete()
    except:
        pass

    print "Removing platform clone"
    try:
        plat = org.platforms().get_resource("newName")
        plat.delete()
    except:
        pass

    print "Removing environment clone"
    try:
        env = org.environments().get_resource("newName")
        for h in env.hosts().get_resources():
            h.delete()
        env.delete()
    except:
        pass

    print "Removing host clone"
    env = org.environments().get_resource(gvs.env_name)
    try:
        host = env.hosts().get_resource(gvs.host_name + " (1)")
        host.delete()
    except:
        pass

def test():
    setup()
    run()
    tear_down()

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
