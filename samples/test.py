#
# Creates resources, provisions a host and then deletes resources using
# cortex-client API.
#

import test_utils, setup, definitions, delete, create, provision

import test_webserver
import test_simple_settings

test_modules = \
    [
        test_webserver.__name__,
        test_simple_settings.__name__
     ]

if __name__ == "__main__":
    # Setup
    setup.setup()
    setup.create_kickstart()
    definitions.define()

    # Clear previous data
    delete.delete_resources()

    # Setup new test environment
    create.create_resources()
    provision.provision_host()

    # Run tests
    test_utils.test_wrapper(test_modules)

    # Tear down test environment
    delete.delete_resources()
    setup.delete_kickstart()
