# coding: utf-8

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class AbstractParametersController(ResourceController):

    _template = "parameter.json"

    def __init__(self):
        super(AbstractParametersController, self).__init__()

    def get_collection(self, argv):
        res = self._get_owning_resource(argv)
        return res.parameters()

    def _print_resource_completions(self, param_num, argv):
        file_pos = self._get_parameter_position()
        if param_num < file_pos:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > file_pos - 1 and param_num == file_pos:
            res = self._get_owning_resource(argv)
            self._print_identifiers(res.parameters())


class ApplicationParametersController(AbstractParametersController):

    def __init__(self):
        super(ApplicationParametersController, self).__init__()

    def _get_parameter_position(self):
        return 2

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an application and a parameter name must be provided");
        return argv[2]

    def _get_owning_resource(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and an application name must be provided");

        org = self._api.organizations().get_resource(argv[0])
        return org.applications().get_resource(argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.applications())

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <app_name>
                            List all parameters of a given application
    show <org_name> <app_name> <file_name>
                            Show the details of a parameter
    add <org_name> <app_name> <file_name>
                            Add a parameter
    update <org_name> <app_name> <file_name>
                            Update a parameter
    delete <org_name> <app_name> <file_name>
                            Delete a parameter
'''


class DistributionParametersController(AbstractParametersController):

    def __init__(self):
        super(DistributionParametersController, self).__init__()

    def _get_parameter_position(self):
        return 2

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, a distribution and a parameter name must be provided");
        return argv[2]

    def _get_owning_resource(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a distribution name must be provided");

        org = self._api.organizations().get_resource(argv[0])
        return org.distributions().get_resource(argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.distributions())

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <app_name>
                            List all parameters of a given distribution
    show <org_name> <app_name> <file_name>
                            Show the details of a parameter
    add <org_name> <app_name> <file_name>
                            Add a parameter
    update <org_name> <app_name> <file_name>
                            Update a parameter
    delete <org_name> <app_name> <file_name>
                            Delete a parameter
'''


class PlatformParametersController(AbstractParametersController):

    def __init__(self):
        super(PlatformParametersController, self).__init__()

    def _get_parameter_position(self):
        return 2

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, a platform and a parameter must be provided");
        return argv[2]

    def _get_owning_resource(self, argv):
        if len(argv) < 2:
            raise ArgumentException("An organization and a platform name must be provided");

        org = self._api.organizations().get_resource(argv[0])
        return org.platforms().get_resource(argv[1])

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.platforms())

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <app_name>
                            List all parameters of a given platform
    show <org_name> <app_name> <file_name>
                            Show the details of a parameter
    add <org_name> <app_name> <file_name>
                            Add a parameter
    update <org_name> <app_name> <file_name>
                            Update a parameter
    delete <org_name> <app_name> <file_name>
                            Delete a parameter
'''
