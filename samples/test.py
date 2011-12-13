#
# Creates resources, provisions a host and then deletes resources using
# cortex-client API.
#

import create, delete, provision, do_demo

if __name__ == "__main__":
    create.create_resources()
    provision.provision_host()
    do_demo.do_demo()
    delete.delete_resources()
