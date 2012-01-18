# coding: utf-8

from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException

class AbstractFilesController(ResourceController):

    _template = "file.json"

    def __init__(self):
        super(AbstractFilesController, self).__init__()

        self._register(["show-content"], self._show_content, self._print_resource_completions)
        self._register(["set-content"], self._set_content, self._print_resource_completions)

    def get_collection(self, argv):
        res = self._get_owning_resource(argv)
        return res.files()

    def _print_resource_completions(self, param_num, argv):
        file_pos = self._get_file_position()
        if param_num < file_pos:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > file_pos - 1 and param_num == file_pos:
            res = self._get_owning_resource(argv)
            self._print_identifiers(res.files())

    def _show_content(self, argv):
        file_res = self._get_resource(argv)
        print file_res.get_content().read()

    def _set_content(self, argv):
        file_res = self._get_resource(argv)
        file_res.set_content(argv[self._get_path_position()])


class ApplicationFilesController(AbstractFilesController):

    _template = "application_file.json"

    def __init__(self):
        super(ApplicationFilesController, self).__init__()

    def _get_file_position(self):
        return 2

    def _get_path_position(self):
        return 3

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, an application and a file name must be provided");
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
                            List all file resources of a given application
    show <org_name> <app_name> <file_name>
                            Show the details of a file resource
    add <org_name> <app_name> <file_name>
                            Add a file resource
    update <org_name> <app_name> <file_name>
                            Update a file resource
    delete <org_name> <app_name> <file_name>
                            Delete a file resource
'''


class DistributionFilesController(AbstractFilesController):

    def __init__(self):
        super(DistributionFilesController, self).__init__()

    def _get_file_position(self):
        return 2

    def _get_path_position(self):
        return 3

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("An organization, a distribution and a file name must be provided");
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
                            List all files of a given distribution
    show <org_name> <app_name> <file_name>
                            Show the details of a file
    add <org_name> <app_name> <file_name>
                            Add a file
    update <org_name> <app_name> <file_name>
                            Update a file
    delete <org_name> <app_name> <file_name>
                            Delete a file
'''
