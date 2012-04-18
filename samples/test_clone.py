# Setup Python path
import sys, test_utils
from setup import global_vars as gvs

sys.path.append("..")


#==============================================================================
# Imports section

from cortex_client.api.api import CortexApi


#==============================================================================
# Script

def setup(argv):
    pass

def run(argv):
    api = CortexApi(gvs.comodit_url, gvs.comodit_user, gvs.comodit_pass)

    org = api.organizations().get_resource(gvs.org_name)

    print "Clone application"
    app = org.applications().get_resource(gvs.web_server_name)
    app.clone("newName")
    org.applications().get_resource("newName")

    print "Clone distribution"
    dist = org.distributions().get_resource(gvs.dist_names[0])
    dist.clone("newName")
    org.distributions().get_resource("newName")

    print "Clone platform"
    plat = org.platforms().get_resource(gvs.plat_names[0])
    plat.clone("newName")
    org.platforms().get_resource("newName")

    print "Clone environment"
    env = org.environments().get_resource(gvs.env_name)
    env.clone("newName")
    org.environments().get_resource("newName")

    print "Clone host"
    host = env.hosts().get_resource(argv[0])
    host.clone()
    env.hosts().get_resource(argv[0] + " (1)")

def tear_down(argv):
    api = CortexApi(gvs.comodit_url, gvs.comodit_user, gvs.comodit_pass)

    org = api.organizations().get_resource(gvs.org_name)

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
        host = env.hosts().get_resource(argv[0] + " (1)")
        host.delete()
    except:
        pass

#==============================================================================
# Entry point
if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
