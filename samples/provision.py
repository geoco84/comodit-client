# Setup Python path
import sys, setup
import definitions as defs
sys.path.append("..")


#==============================================================================
# Imports section

import time
import cortex_client.api.collections as collections

from cortex_client.api.api import CortexApi
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def provision_host(host_name):
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi(setup.global_vars.comodit_url, setup.global_vars.comodit_user, setup.global_vars.comodit_pass)

    host = api.organizations().get_resource(setup.global_vars.org_name).environments().get_resource(setup.global_vars.env_name).hosts().get_resource(host_name)
    plat = collections.platforms(api, setup.global_vars.org_name).get_resource(host.get_platform())

    #############
    # Provision #
    #############

    print "="*80
    print "Provisioning host " + host_name
    host.provision()

    print "="*80
    print "Waiting for the end of installation..."

    # With Libvirt driver, VM must be restarted by hand
    if "LibvirtDriver" in plat.get_driver().get_classname():
        state = None
        try:
            state = host.instance().get_single_resource().get_state()
        except PythonApiException, e:
            print e.message
        while state != "STOPPED":
            time.sleep(3)
            try:
                state = host.instance().get_single_resource().get_state()
            except PythonApiException, e:
                print e.message

        print "="*80
        print "Restarting..."
        host.instance().get_single_resource().start()
        host.update()

    while host.get_state() != "PROVISIONED":
        time.sleep(3)
        host.update()

    print "="*80
    print "Host provisioned and running."

#==============================================================================
# Entry point
if __name__ == "__main__":
    setup.setup()
    defs.define()
    provision_host(sys.argv[1])
