import sys
from StringIO import StringIO

import test_utils
import setup as test_setup
import definitions as defs

from setup import global_vars as gvs

sys.path.append("..")

import cortex_client.api.collections as collections

from cortex_client import dispatch
from cortex_client.api.api import CortexApi

def setup(argv):
    pass

def tear_down(argv):
    pass

def test_client(expected_code = 0):
    mystdout = StringIO()
    sys.stdout = mystdout
    argv = sys.argv[1:]
    error = False
    try:
        dispatch.run(argv)
    except SystemExit, e:
        if e.code != expected_code:
            error = True
            raise Exception("Unexpected exit code " + str(e.code))
    finally:
        sys.stdout = sys.__stdout__
        if error:
            print "--- BEGIN OUTPUT"
            print mystdout.getvalue()
            print "--- END OUTPUT"

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)
    org = api.organizations().get_resource(gvs.org_name)

    # Organizations (read)
    print "Testing organizations list"
    sys.argv = ["cortex", "organizations", "list"]
    test_client()

    print "Testing organizations show"
    sys.argv = ["cortex", "organizations", "show", gvs.org_name]
    test_client()

    print "Testing organizations settings list"
    sys.argv = ["cortex", "organizations", "settings", "list", gvs.org_name]
    test_client()

    print "Testing organizations settings show"
    for s in org.get_settings():
        sys.argv = ["cortex", "organizations", "settings", "show", gvs.org_name, s.get_name()]
        test_client()

    # Applications (read)
    print "Testing applications list"
    sys.argv = ["cortex", "applications", "list", gvs.org_name]
    test_client()

    print "Testing applications show"
    for app_name in gvs.app_names:
        print "  " + app_name
        sys.argv = ["cortex", "applications", "show", gvs.org_name, app_name]
        test_client()

    print "Testing application files list"
    for app_name in gvs.app_names:
        print "  " + app_name
        sys.argv = ["cortex", "applications", "files", "list", gvs.org_name, app_name]
        test_client()

    print "Testing application files show"
    for app_name in gvs.app_names:
        print "  " + app_name
        app = org.applications().get_resource(app_name)
        for f in app.get_files():
            f_name = f.get_name()
            print "    " + f_name
            sys.argv = ["cortex", "applications", "files", "show", gvs.org_name, app_name, f_name]
            test_client()

    print "Testing application files show-content"
    for app_name in gvs.app_names:
        print "  " + app_name
        app = org.applications().get_resource(app_name)
        for f in app.get_files():
            f_name = f.get_name()
            print "    " + f_name
            sys.argv = ["cortex", "applications", "files", "show-content", gvs.org_name, gvs.web_server_name, "httpd.conf"]
            test_client()

    print "Testing application parameters list"
    for app_name in gvs.app_names:
        print "  " + app_name
        sys.argv = ["cortex", "applications", "parameters", "list", gvs.org_name, app_name]
        test_client()

    print "Testing application parameters show"
    for app_name in gvs.app_names:
        print "  " + app_name
        sys.argv = ["cortex", "applications", "parameters", "show", gvs.org_name, gvs.web_server_name, "Httpd Port"]
        test_client()


    # Platforms (read)
    print "Testing platforms list"
    sys.argv = ["cortex", "platforms", "list", gvs.org_name]
    test_client()

    print "Testing platforms show"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        sys.argv = ["cortex", "platforms", "show", gvs.org_name, plat_name]
        test_client()

    print "Testing platforms files list"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        sys.argv = ["cortex", "platforms", "files", "list", gvs.org_name, plat_name]
        test_client()

    print "Testing platforms files show"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        plat = collections.platforms(api, gvs.org_name).get_resource(plat_name)
        for f in plat.get_files():
            sys.argv = ["cortex", "platforms", "files", "show", gvs.org_name, plat_name, f.get_name()]
            test_client()

    print "Testing platforms files show-content"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        plat = collections.platforms(api, gvs.org_name).get_resource(plat_name)
        for f in plat.get_files():
            sys.argv = ["cortex", "platforms", "files", "show-content", gvs.org_name, plat_name, f.get_name()]
            test_client()

    print "Testing platforms parameters list"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        plat = collections.platforms(api, gvs.org_name).get_resource(plat_name)
        sys.argv = ["cortex", "platforms", "parameters", "list", gvs.org_name, plat_name]
        test_client()

    print "Testing platforms parameters show"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        plat = collections.platforms(api, gvs.org_name).get_resource(plat_name)
        for p in plat.get_parameters():
            sys.argv = ["cortex", "platforms", "parameters", "show", gvs.org_name, plat_name, p.get_name()]
            test_client()

    print "Testing platforms settings list"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        plat = collections.platforms(api, gvs.org_name).get_resource(plat_name)
        sys.argv = ["cortex", "platforms", "settings", "list", gvs.org_name, plat_name]
        test_client()

    print "Testing platforms settings show"
    for plat_name in gvs.plat_names:
        print "  " + plat_name
        plat = collections.platforms(api, gvs.org_name).get_resource(plat_name)
        for s in plat.get_settings():
            sys.argv = ["cortex", "platforms", "settings", "show", gvs.org_name, plat_name, s.get_name()]
            test_client()


    # Distributions (read)
    print "Testing distributions list"
    sys.argv = ["cortex", "distributions", "list", gvs.org_name]
    test_client()

    print "Testing distributions show"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        sys.argv = ["cortex", "distributions", "show", gvs.org_name, dist_name]
        test_client()

    print "Testing distributions files list"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        sys.argv = ["cortex", "distributions", "files", "list", gvs.org_name, dist_name]
        test_client()

    print "Testing distributions files show"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        dist = collections.distributions(api, gvs.org_name).get_resource(dist_name)
        for f in dist.get_files():
            sys.argv = ["cortex", "distributions", "files", "show", gvs.org_name, dist_name, f.get_name()]
            test_client()

    print "Testing distributions files show-content"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        dist = collections.distributions(api, gvs.org_name).get_resource(dist_name)
        for f in dist.get_files():
            sys.argv = ["cortex", "distributions", "files", "show-content", gvs.org_name, dist_name, f.get_name()]
            test_client()

    print "Testing distributions parameters list"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        sys.argv = ["cortex", "distributions", "parameters", "list", gvs.org_name, dist_name]
        test_client()

    print "Testing distributions parameters show"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        dist = collections.distributions(api, gvs.org_name).get_resource(dist_name)
        for p in dist.get_parameters():
            sys.argv = ["cortex", "distributions", "parameters", "show", gvs.org_name, dist_name, p.get_name()]
            test_client()

    print "Testing distributions settings list"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        sys.argv = ["cortex", "distributions", "settings", "list", gvs.org_name, dist_name]
        test_client()

    print "Testing distributions settings show"
    for dist_name in gvs.dist_names:
        print "  " + dist_name
        dist = collections.distributions(api, gvs.org_name).get_resource(dist_name)
        for s in dist.get_settings():
            sys.argv = ["cortex", "distributions", "settings", "show", gvs.org_name, dist_name, s.get_name()]
            test_client()


    # Environments (read)
    print "Testing environments list"
    sys.argv = ["cortex", "environments", "list", gvs.org_name]
    test_client()

    print "Testing environments show"
    sys.argv = ["cortex", "environments", "show", gvs.org_name, gvs.env_name]
    test_client()

    print "Testing environments settings list"
    sys.argv = ["cortex", "environments", "settings", "list", gvs.org_name, gvs.env_name]
    test_client()

    print "Testing environments settings show"
    env = org.environments().get_resource(gvs.env_name)
    for s in env.get_settings():
        sys.argv = ["cortex", "environments", "settings", "show", gvs.org_name, gvs.env_name, s.get_key()]
        test_client()


    # Hosts (read)
    print "Testing hosts list"
    sys.argv = ["cortex", "hosts", "list", gvs.org_name, gvs.env_name]
    test_client()

    print "Testing hosts show"
    for host_name in defs.get_host_names():
        sys.argv = ["cortex", "hosts", "show", gvs.org_name, gvs.env_name, host_name]
        test_client()

    print "Testing hosts settings list"
    for host_name in defs.get_host_names():
        sys.argv = ["cortex", "hosts", "settings", "list", gvs.org_name, gvs.env_name, host_name]
        test_client()

    print "Testing hosts settings show"
    for host_name in defs.get_host_names():
        host = collections.hosts(api, gvs.org_name, gvs.env_name).get_resource(host_name)
        for s in host.get_settings():
            sys.argv = ["cortex", "hosts", "settings", "show", gvs.org_name, gvs.env_name, host_name, s.get_key()]
            test_client()

if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
