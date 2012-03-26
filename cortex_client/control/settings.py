# coding: utf-8

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException
from cortex_client.api import collections

class HostAbstractSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(HostAbstractSettingsController, self).__init__()

        self._doc = "Settings handling."
        self._update_action_doc_params("list", "<org_name> <env_name> <host_name>")
        self._update_action_doc_params("add", "<org_name> <env_name> <host_name>")
        self._update_action_doc_params("delete", "<org_name> <env_name> <host_name> <setting_name>")
        self._update_action_doc_params("update", "<org_name> <env_name> <host_name> <setting_name>")
        self._update_action_doc_params("show", "<org_name> <env_name> <host_name> <setting_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 4:
            raise ArgumentException("An organization, an environment, a host and a setting name must be provided");

        return argv[3]

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an environment and a host must be provided");

        host = collections.hosts(self._api, argv[0], argv[1]).get_resource(argv[2])
        return self._get_settings(host, argv)

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.environments())
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(collections.hosts(self._api, argv[0], argv[1]))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            host = collections.hosts(self._api, argv[0], argv[1]).get_resource(argv[2])
            self._print_identifiers(self._get_settings(host, argv))


class PlatformContextSettingsController(HostAbstractSettingsController):

    def __init__(self):
        super(PlatformContextSettingsController, self).__init__()

    def _get_settings(self, host, argv):
        return host.platform().get_single_resource().settings()


class DistributionContextSettingsController(HostAbstractSettingsController):

    def __init__(self):
        super(DistributionContextSettingsController, self).__init__()

    def _get_settings(self, host, argv):
        return host.distribution().get_single_resource().settings()


class ApplicationContextSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(ApplicationContextSettingsController, self).__init__()

        self._doc = "Settings handling."

        self._update_action_doc_params("list", "<org_name> <env_name> <host_name> <app_name>")
        self._update_action_doc_params("add", "<org_name> <env_name> <host_name> <app_name>")
        self._update_action_doc_params("delete", "<org_name> <env_name> <host_name> <app_name> <setting_name>")
        self._update_action_doc_params("update", "<org_name> <env_name> <host_name> <app_name> <setting_name>")
        self._update_action_doc_params("show", "<org_name> <env_name> <host_name> <app_name> <setting_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 5:
            raise ArgumentException("An organization, an environment, a host, an application and a setting name must be provided");

        return argv[4]

    def get_collection(self, argv):
        if len(argv) < 4:
            raise ArgumentException("An organization, an environment, a host and an application name must be provided");

        return collections.application_contexts(self._api, argv[0], argv[1], argv[2]).get_resource(argv[3]).settings()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.environments(self._api, argv[0]))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(collections.hosts(self._api, argv[0], argv[1]))
        elif len(argv) > 2 and param_num == 3:
            host = collections.hosts(self._api, argv[0], argv[1]).get_resource(argv[2])
            self._print_escaped_names(host.get_applications())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 4:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 3 and param_num == 4:
            self._print_identifiers(collections.app_context_settings(self._api, argv[0], argv[1], argv[2], argv[3]))


class HostSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(HostSettingsController, self).__init__()

        self._doc = "Settings handling."
        self._update_action_doc_params("list", "<org_name> <env_name> <host_name>")
        self._update_action_doc_params("add", "<org_name> <env_name> <host_name>")
        self._update_action_doc_params("delete", "<org_name> <env_name> <host_name> <setting_name>")
        self._update_action_doc_params("update", "<org_name> <env_name> <host_name> <setting_name>")
        self._update_action_doc_params("show", "<org_name> <env_name> <host_name> <setting_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 4:
            raise ArgumentException("An organization, an environment, a host and a setting name must be provided");

        return argv[3]

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an environment and a host name must be provided");

        return collections.host_settings(self._api, argv[0], argv[1], argv[2])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.environments(self._api, argv[0]))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(collections.hosts(self._api, argv[0], argv[1]))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            self._print_identifiers(collections.host_settings(self._api, argv[0], argv[1], argv[2]))


class EnvironmentSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(EnvironmentSettingsController, self).__init__()

        self._doc = "Settings handling."
        self._update_action_doc_params("list", "<org_name> <env_name>")
        self._update_action_doc_params("add", "<org_name> <env_name>")
        self._update_action_doc_params("delete", "<org_name> <env_name> <setting_name>")
        self._update_action_doc_params("update", "<org_name> <env_name> <setting_name>")
        self._update_action_doc_params("show", "<org_name> <env_name> <setting_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an environment and a setting name must be provided");

        return argv[2]

    def get_collection(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and an environment must be provided");

        return collections.env_settings(self._api, argv[0], argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.environments(self._api, argv[0]))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 2:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(collections.env_settings(self._api, argv[0], argv[1]))


class DistributionSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(DistributionSettingsController, self).__init__()

        self._doc = "Settings handling."
        self._update_action_doc_params("list", "<org_name> <dist_name>")
        self._update_action_doc_params("add", "<org_name> <dist_name>")
        self._update_action_doc_params("delete", "<org_name> <dist_name> <setting_name>")
        self._update_action_doc_params("update", "<org_name> <dist_name> <setting_name>")
        self._update_action_doc_params("show", "<org_name> <dist_name> <setting_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, a distribution and a setting name must be provided");

        return argv[2]

    def get_collection(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a distribution must be provided");

        return collections.dist_settings(self._api, argv[0], argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.distributions(self._api, argv[0]))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 2:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(collections.dist_settings(self._api, argv[0], argv[1]))


class PlatformSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(PlatformSettingsController, self).__init__()

        self._doc = "Settings handling."
        self._update_action_doc_params("list", "<org_name> <plat_name>")
        self._update_action_doc_params("add", "<org_name> <plat_name>")
        self._update_action_doc_params("delete", "<org_name> <plat_name> <setting_name>")
        self._update_action_doc_params("update", "<org_name> <plat_name> <setting_name>")
        self._update_action_doc_params("show", "<org_name> <plat_name> <setting_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, a platform and a setting name must be provided");

        return argv[2]

    def get_collection(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a platform must be provided");

        return collections.plat_settings(self._api, argv[0], argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.platforms(self._api, argv[0]))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 2:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(collections.plat_settings(self._api, argv[0], argv[1]))


class OrganizationSettingsController(ResourceController):

    _template = "setting.json"

    def __init__(self):
        super(OrganizationSettingsController, self).__init__()

        self._doc = "Settings handling."
        self._update_action_doc_params("list", "<org_name>")
        self._update_action_doc_params("add", "<org_name>")
        self._update_action_doc_params("delete", "<org_name> <setting_name>")
        self._update_action_doc_params("update", "<org_name> <setting_name>")
        self._update_action_doc_params("show", "<org_name> <setting_name>")

    def _get_name_argument(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a setting name must be provided");

        return argv[1]

    def get_collection(self, argv):
        if len(argv) < 1:
            raise ArgumentException("An organization must be provided");

        return collections.org_settings(self._api, argv[0])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 1:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(collections.org_settings(self._api, argv[0]))
