# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.exceptions import ArgumentException
from cortex_client.control.resource import ResourceController
from cortex_client.control.settings import ApplicationContextSettingsController, \
    PlatformContextSettingsController, DistributionContextSettingsController

class ApplicationContextController(ResourceController):

    _template = "application_context.json"

    def __init__(self):
        super(ApplicationContextController, self).__init__()

        # subcontroller
        self._register_subcontroller(["settings"], ApplicationContextSettingsController())

        # actions
        self._register(["install"], self._install, self._print_install_completions)
        self._register(["uninstall"], self._uninstall, self._print_resource_completions)

        # 'install' and 'uninstall' are aliases for 'add' and 'delete'
        self._unregister(["add", "delete"])

        self._doc = "Application contexts handling."

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])
        return host.applications()

    def _complete_template(self, argv, template_json):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments");
        template_json["application"] = argv[3]

    def _get_name_argument(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments");

        return argv[3]

    def _get_environments(self, argv):
        org = self._api.organizations().get_resource(argv[0])
        return org.environments()

    def _get_hosts(self, argv):
        env = self._get_environments(argv).get_resource(argv[1])
        return env.hosts()

    def _get_host(self, argv):
        return self._get_hosts(argv).get_resource(argv[2])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(self._get_environments(argv))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(self._get_hosts(argv))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            self._print_identifiers(host.applications())

    def _print_install_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.applications())

    def _install(self, argv):
        self._add(argv)

    def _uninstall(self, argv):
        self._delete(argv)

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>          List all application profiles available to the user
    show <org_name> <app_name>
                             Show the details of an application
    install <org_name> <env_name> <host_name> <app_name>
                            Installs an application on a given host
    uninstall <org_name> <env_name> <host_name> <app_name>
                            Uninstalls an application on a given host
'''


class PlatformContextController(ResourceController):

    _template = "platform_context.json"

    def __init__(self):
        super(PlatformContextController, self).__init__()

        # subcontroller
        self._register_subcontroller(["settings"], PlatformContextSettingsController())

        self._unregister(["update", "list"])

        self._doc = "Distribution contexts handling."

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])
        return host.platform()

    def _get_name_argument(self, argv):
        return ""

    def _get_environments(self, argv):
        org = self._api.organizations().get_resource(argv[0])
        return org.environments()

    def _get_hosts(self, argv):
        env = self._get_environments(argv).get_resource(argv[1])
        return env.hosts()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(self._get_environments(argv))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(self._get_hosts(argv))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    add <org_name> <env_name> <host_name>
                                Add a platform context to a host
    delete <org_name> <env_name> <host_name>
                                Delete the platform context of a host
    show <org_name> <env_name> <host_name>
                                Show the platform context of a host
    settings <...>
                                Settings handling
'''

class DistributionContextController(ResourceController):

    _template = "distribution_context.json"

    def __init__(self):
        super(DistributionContextController, self).__init__()

        # subcontroller
        self._register_subcontroller(["settings"], DistributionContextSettingsController())

        self._unregister(["update", "list"])

        self._doc = "Distribution contexts handling."

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])
        return host.distribution()

    def _get_name_argument(self, argv):
        return ""

    def _get_environments(self, argv):
        org = self._api.organizations().get_resource(argv[0])
        return org.environments()

    def _get_hosts(self, argv):
        env = self._get_environments(argv).get_resource(argv[1])
        return env.hosts()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(self._get_environments(argv))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(self._get_hosts(argv))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    add <org_name> <env_name> <host_name>
                                Add a distribution context to a host
    delete <org_name> <env_name> <host_name>
                                Delete the distribution context of a host
    show <org_name> <env_name> <host_name>
                                Show the distribution context of a host
    settings <...>
                                Settings handling
'''
