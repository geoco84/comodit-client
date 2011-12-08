# coding: utf-8

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class ApplicationSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(ApplicationSettingsController, self).__init__()

    def _get_name_argument(self, argv):
        if len(argv) < 5:
            raise ArgumentException("An organization, an environment, a host, an application and a setting name must be provided");

        return argv[4]

    def get_collection(self, argv):
        if len(argv) < 4:
            raise ArgumentException("An organization, an environment, a host and an application name must be provided");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])
        app = host.applications().get_resource(argv[3])

        return app.settings()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.environments())
        elif len(argv) > 1 and param_num == 2:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            self._print_identifiers(env.hosts())
        elif len(argv) > 2 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            self._print_escaped_names(host.applications())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 4:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 3 and param_num == 4:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            self._print_identifiers(host.application_settings(argv[3]))

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <env_name> <host_name> <app_name>
                            List all settings of a given application
    show <org_name> <env_name> <host_name> <app_name> <setting_name>
                            Show the details of a setting
    add <org_name> <env_name> <host_name> <app_name>
                            Add a setting
    update <org_name> <env_name> <host_name> <app_name> <setting_name>
                            Update a setting
    delete <org_name> <env_name> <host_name> <app_name> <setting_name>
                            Delete a setting
'''


class HostSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(HostSettingsController, self).__init__()

    def _get_name_argument(self, argv):
        if len(argv) < 4:
            raise ArgumentException("An organization, an environment, a host and a setting name must be provided");

        return argv[3]

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an environment and a host name must be provided");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])

        return host.settings()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.environments())
        elif len(argv) > 1 and param_num == 2:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            self._print_identifiers(env.hosts())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            self._print_identifiers(host.settings())

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <env_name> <host_name>
                            List all settings of a given host
    show <org_name> <env_name> <host_name> <setting_name>
                            Show the details of a setting
    add <org_name> <env_name> <host_name>
                            Add a setting
    update <org_name> <env_name> <host_name> <setting_name>
                            Update a setting
    delete <org_name> <env_name> <host_name> <setting_name>
                            Delete a setting
'''


class EnvironmentSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(EnvironmentSettingsController, self).__init__()

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an environment and a setting name must be provided");

        return argv[2]

    def get_collection(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and an environment must be provided");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])

        return env.settings()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.environments())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 2:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 1 and param_num == 2:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            self._print_identifiers(env.settings())

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <env_name>
                            List all settings of a given environment
    show <org_name> <env_name> <setting_name>
                            Show the details of a setting
    add <org_name> <env_name>
                            Add a setting
    update <org_name> <env_name> <setting_name>
                            Update a setting
    delete <org_name> <env_name> <setting_name>
                            Delete a setting
'''


class OrganizationSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(OrganizationSettingsController, self).__init__()

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a setting name must be provided");

        return argv[1]

    def get_collection(self, argv):
        if len(argv) < 1:
            raise ArgumentException("An organization must be provided");

        org = self._api.organizations().get_resource(argv[0])

        return org.settings()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 1:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.settings())

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name>
                            List all settings of a given environment
    show <org_name> <setting_name>
                            Show the details of a setting
    add <org_name>
                            Add a setting
    update <org_name> <setting_name>
                            Update a setting
    delete <org_name> <setting_name>
                            Delete a setting
'''
