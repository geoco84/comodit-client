# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.api import collections
from cortex_client.control.abstract import AbstractController
from cortex_client.control.exceptions import ArgumentException
from cortex_client.control.doc import ActionDoc

class LiveController(AbstractController):

    def __init__(self):
        super(LiveController, self).__init__()
        self._doc = "Live management."

        self._register(["update-file"], self._update_file, self._print_file_completions)
        self._register(["restart-service"], self._restart_service, self._print_service_completions)
        self._register(["install-package"], self._install_package, self._print_package_completions)
        self._register(["help"], self._help)
        self._default_action = self._help

        self._register_action_doc(self._update_file_doc())
        self._register_action_doc(self._restart_service_doc())
        self._register_action_doc(self._install_package_doc())

    def _help(self, argv):
        self._print_doc()

    def _print_host_completions(self, param_num, argv):
        if param_num == 0:
            self._print_resource_identifiers(collections.organizations(self._api).get_resources())
        elif len(argv) > 0 and param_num == 1:
            self._print_resource_identifiers(collections.environments(self._api, argv[0]).get_resources())
        elif len(argv) > 1 and param_num == 2:
            self._print_resource_identifiers(collections.hosts(self._api, argv[0], argv[1]).get_resources())

    def _print_file_completions(self, param_num, argv):
        if param_num < 3:
            self._print_host_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            host = collections.hosts(self._api, argv[0], argv[1]).get_resource(argv[2])
            self._print_escaped_names(self._get_file_resources(host))

    def _print_service_completions(self, param_num, argv):
        if param_num < 3:
            self._print_host_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            host = collections.hosts(self._api, argv[0], argv[1]).get_resource(argv[2])
            self._print_escaped_names(self._get_service_resources(host))

    def _print_package_completions(self, param_num, argv):
        if param_num < 3:
            self._print_host_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            host = collections.hosts(self._api, argv[0], argv[1]).get_resource(argv[2])
            self._print_escaped_names(self._get_package_resources(host))

    def _get_file_resources(self, host):
        res_list = []
        apps = host.get_applications()
        for app_name in apps:
            app = collections.applications(self._api, host.get_organization()).get_resource(app_name)
            files = app.get_files()
            for f in files:
                res_list.append(f.get_path())

        return res_list

    def _get_package_resources(self, host):
        res_list = []
        apps = host.get_applications()
        for app_name in apps:
            app = collections.applications(self._api, host.get_organization()).get_resource(app_name)
            packages = app.get_packages()
            for p in packages:
                res_list.append(p.get_name())

        return res_list

    def _get_service_resources(self, host):
        res_list = []
        apps = host.get_applications()
        for app_name in apps:
            app = collections.applications(self._api, host.get_organization()).get_resource(app_name)
            services = app.get_services()
            for s in services:
                res_list.append(s.get_name())

        return res_list

    def _get_host(self, argv):
        return collections.hosts(self._api, argv[0], argv[1]).get_resource(argv[2])

    def _update_file(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments")

        host = self._get_host(argv)
        id = argv[3].replace("/", "%2f")
        host.do_live("files", id)

    def _update_file_doc(self):
        return ActionDoc("udpate-file", "<org_name> <env_name> <host_name> <file_path>", """
        Updates file on given host.""")

    def _restart_service(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments")

        host = self._get_host(argv)
        id = argv[3]
        host.do_live("services", id)

    def _restart_service_doc(self):
        return ActionDoc("restart-service", "<org_name> <env_name> <host_name> <service_name>", """
        Restarts service on given host.""")

    def _install_package(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments")

        host = self._get_host(argv)
        id = argv[3]
        host.do_live("packages", id)

    def _install_package_doc(self):
        return ActionDoc("install-package", "<org_name> <env_name> <host_name> <package_name>", """
        Install package on given host.""")
