import sys
from StringIO import StringIO

import test_utils
import setup as test_setup

from definitions import global_vars as gvs
from test_simple_settings import add_simple_setting, delete_setting

sys.path.append("..")

from cortex_client import dispatch
from cortex_client.api.api import CortexApi

def setup(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(gvs.org_name)
    env = org.environments().get_resource(gvs.env_name)
    add_simple_setting(env, "test_key", "value")

def tear_down(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)

    org = api.organizations().get_resource(gvs.org_name)
    env = org.environments().get_resource(gvs.env_name)
    delete_setting(env, "test_key")

def test_client(expected_code = 0):
    mystdout = StringIO()
    sys.stdout = mystdout
    argv = sys.argv[1:]
    try:
        dispatch.run(argv)
    except SystemExit, e:
        if e.code != expected_code:
            raise Exception("Unexpected exit code")
    finally:
        sys.stdout = sys.__stdout__

def run(argv):
    api = CortexApi(test_setup.global_vars.comodit_url, test_setup.global_vars.comodit_user, test_setup.global_vars.comodit_pass)
    org = api.organizations().get_resource(gvs.org_name)

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
    sys.argv = ["cortex", "platforms", "show", gvs.org_name, gvs.plat_name]
    test_client()

    print "Testing platforms files list"
    sys.argv = ["cortex", "platforms", "files", "list", gvs.org_name, gvs.plat_name]
    test_client()

    print "Testing platforms files show"
    sys.argv = ["cortex", "platforms", "files", "show", gvs.org_name, gvs.plat_name, "libvirt.domain.fmt"]
    test_client()

    print "Testing platforms files show-content"
    sys.argv = ["cortex", "platforms", "files", "show-content", gvs.org_name, gvs.plat_name, "libvirt.domain.fmt"]
    test_client()

    print "Testing platforms parameters list"
    sys.argv = ["cortex", "platforms", "parameters", "list", gvs.org_name, gvs.plat_name]
    test_client()

    print "Testing platforms parameters show"
    sys.argv = ["cortex", "platforms", "parameters", "show", gvs.org_name, gvs.plat_name, "Memory"]
    test_client()

    print "Testing platforms settings list"
    sys.argv = ["cortex", "platforms", "settings", "list", gvs.org_name, gvs.plat_name]
    test_client()

    print "Testing platforms settings show"
    sys.argv = ["cortex", "platforms", "settings", "show", gvs.org_name, gvs.plat_name, "libvirt.connectUrl"]
    test_client()


    # Distributions (read)
    print "Testing distributions list"
    sys.argv = ["cortex", "distributions", "list", gvs.org_name]
    test_client()

    print "Testing distributions show"
    sys.argv = ["cortex", "distributions", "show", gvs.org_name, gvs.dist_name]
    test_client()

    print "Testing distributions files list"
    sys.argv = ["cortex", "distributions", "files", "list", gvs.org_name, gvs.dist_name]
    test_client()

    print "Testing distributions files show"
    dist = org.distributions().get_resource(gvs.dist_name)
    dist_files = dist.get_files()
    for f in dist_files:
        name = f.get_name()
        print "  " + name
        sys.argv = ["cortex", "distributions", "files", "show", gvs.org_name, gvs.dist_name, name]
        test_client()

    print "Testing distributions files show-content"
    dist = org.distributions().get_resource(gvs.dist_name)
    dist_files = dist.get_files()
    for f in dist_files:
        name = f.get_name()
        print "  " + name
        sys.argv = ["cortex", "distributions", "files", "show-content", gvs.org_name, gvs.dist_name, name]
        test_client()

    print "Testing distributions parameters list"
    sys.argv = ["cortex", "distributions", "parameters", "list", gvs.org_name, gvs.dist_name]
    test_client()

    print "Testing distributions parameters show"
    sys.argv = ["cortex", "distributions", "parameters", "show", gvs.org_name, gvs.dist_name, "Zone"]
    test_client()

    print "Testing distributions settings list"
    sys.argv = ["cortex", "distributions", "settings", "list", gvs.org_name, gvs.dist_name]
    test_client()

    print "Testing distributions settings show"
    sys.argv = ["cortex", "distributions", "settings", "show", gvs.org_name, gvs.dist_name, "initrd_path"]
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
    sys.argv = ["cortex", "environments", "settings", "show", gvs.org_name, gvs.env_name, "test_key"]
    test_client()


    # Hosts (read)
    print "Testing hosts list"
    sys.argv = ["cortex", "hosts", "list", gvs.org_name, gvs.env_name]
    test_client()

    print "Testing hosts show"
    sys.argv = ["cortex", "hosts", "show", gvs.org_name, gvs.env_name, argv[0]]
    test_client()

    print "Testing hosts changes"
    sys.argv = ["cortex", "hosts", "changes", gvs.org_name, gvs.env_name, argv[0]]
    test_client()

    print "Testing hosts clear-changes"
    sys.argv = ["cortex", "hosts", "clear-changes", gvs.org_name, gvs.env_name, argv[0]]
    test_client()

    print "Testing hosts settings list"
    sys.argv = ["cortex", "hosts", "settings", "list", gvs.org_name, gvs.env_name, argv[0]]
    test_client()

    print "Testing hosts settings show"
    sys.argv = ["cortex", "hosts", "settings", "show", gvs.org_name, gvs.env_name, argv[0], "vm_arch"]
    test_client()

if __name__ == "__main__":
    test_utils.test_wrapper([__name__])
