#==============================================================================
# This file illustrates the use of Python API to handle cortex entities.
# Definitions section (after imports) provides the description of several
# entities this script will create (it may need to be updated).
# Script section (after definitions) contains the actual operations (entities
# creation, host provisioning, shutdown and entities removal).
#==============================================================================

# Setup Python path
import sys
sys.path.append("..")


#==============================================================================
# Imports section

import time

from cortex_client.api.api import CortexApi

from definitions import *


#==============================================================================
# Script

def provision_host():
    # API from server cortex listening on port 8000 of localhost is used
    # Username "admin" and password "secret" are used for authentification
    api = CortexApi("http://localhost:8000/api", "admin", "secret")


    host_coll = api.get_host_collection()
    host = host_coll.get_resource_from_path(host_env + "/" + host_name)


    #############
    # Provision #
    #############

    print "="*80
    print "Provisioning host " + host_name
    host.provision()
    host.update()

    print "="*80
    print "Waiting for end of installation..."
    while host.get_instance_info().get_state() == "RUNNING":
        time.sleep(3)

    print "="*80
    print "Restarting..."
    host.start()
    host.update()
    while host.get_state() == "PROVISIONING":
        time.sleep(3)
        host.update()

#==============================================================================
# Entry point
if __name__ == "__main__":
    provision_host()
