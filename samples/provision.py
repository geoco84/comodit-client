# Setup Python path
import sys, setup, time
import definitions as defs
sys.path.append("..")


#==============================================================================
# Imports section

import cortex_client.api.collections as collections

from cortex_client.api.api import CortexApi
from cortex_client.api.exceptions import PythonApiException


#==============================================================================
# Script

def provision_host(host_name, time_out = 0):
    """
    @param time_out: a time out in seconds
    """

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
    print "Waiting for the end of installation on host " + host_name

    # With Libvirt driver, VM must be restarted by hand after installation
    if "LibvirtDriver" in plat.get_driver().get_classname():
        state = None
        try:
            state = host.instance().get_single_resource().get_state()
        except PythonApiException, e:
            print e.message

        start_time = time.time()
        while state != "STOPPED":
            time.sleep(3)

            now = time.time()
            if time_out > 0 and (now - start_time) > time_out:
                raise Exception("Provisioning time-out occurred")

            try:
                state = host.instance().get_single_resource().get_state()
            except PythonApiException, e:
                print e.message

        print "="*80
        print "Restarting " + host_name
        host.instance().get_single_resource().start()
        host.update()

    start_time = time.time()
    while host.get_state() != "READY":
        time.sleep(3)

        now = time.time()
        if time_out > 0 and (now - start_time) > time_out:
                raise Exception("Provisioning time-out occurred")

        host.update()

    print "="*80
    print "Host " + host_name + " provisioned and running."

#==============================================================================
# Entry point
if __name__ == "__main__":
    setup.setup()
    defs.define()
    provision_host(sys.argv[1])
