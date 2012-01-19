# control.hosts - Controller for cortex Hosts resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import json, os

from cortex_client.util import prompt, globals
from cortex_client.util.editor import edit_text
from cortex_client.config import Config
from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException, MissingException
from cortex_client.control.tree_rendering import TreeRenderer
from cortex_client.control.settings import HostSettingsController
from cortex_client.control.instances import InstancesController
from cortex_client.control.contexts import PlatformContextController, \
    DistributionContextController, ApplicationContextController


class HostsController(ResourceController):

    _template = "host.json"

    def __init__(self):
        super(HostsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], HostSettingsController())
        self._register_subcontroller(["instance"], InstancesController())
        self._register_subcontroller(["applications"], ApplicationContextController())
        self._register_subcontroller(["distribution"], DistributionContextController())
        self._register_subcontroller(["platform"], PlatformContextController())

        # actions
        self._register(["provision"], self._provision, self._print_resource_completions)
        self._register(["render-file"], self._render_file, self._print_file_completions)
        self._register(["render-ks"], self._render_ks, self._print_resource_completions)
        self._register(["render-tree"], self._render_tree, self._print_tree_completions)
        self._register(["clone"], self._clone, self._print_resource_completions)
        self._register(["changes"], self._changes, self._print_resource_completions)

    def get_collection(self, argv):
        if len(argv) < 2:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        return env.hosts()

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
            self._print_identifiers(env.hosts())

    def _complete_template(self, argv, template_json):
        if len(argv) < 2:
            raise ArgumentException("Wrong number of arguments");
        template_json["organization"] = argv[0]
        template_json["environment"] = argv[1]

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        return argv[2]

    def _applications(self, argv):
        host = self._get_resource(argv)
        host.show_applications()

    def _delete(self, argv):
        host = self._get_resource(argv)

        if (prompt.confirm(prompt = "Delete " + host.get_name() + " ?", resp = False)) :
            host.delete()

    def _print_file_completions(self, param_num, argv):
        if param_num < 3:
            self._print_resource_completions(param_num, argv)
        elif len(argv) > 2:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])

            if param_num == 3:
                apps = host.get_applications()
                self._print_escaped_names(apps)
            elif len(argv) > 3 and param_num == 4:
                apps = host.get_applications()
                app = org.applications().get_resource(argv[3])
                app_files = app.get_files()
                for f in app_files:
                    self._print_escaped_name(f.get_name())

    def _render_file(self, argv):
        if len(argv) != 5:
            raise ArgumentException("Wrong number of arguments");

        host = self._get_resource(argv)
        app_name = argv[3]
        file_name = argv[4]

        print host.render_file(app_name, file_name).read()

    def _render_ks(self, argv):
        host = self._get_resource(argv)
        print host.render_kickstart().read()

    def _print_tree_completions(self, param_num, argv):
        if param_num < 3:
            self._print_resource_completions(param_num, argv)
        elif param_num == 3:
            self._print_dir_completions()

    def _render_tree(self, argv):
        if len(argv) != 4:
            raise MissingException("This action takes 4 arguments")

        org_name = argv[0]
        env_name = argv[1]
        host_name = argv[2]
        root_dir = argv[3]

        renderer = TreeRenderer(self._api, org_name, env_name, host_name)

        options = globals.options
        renderer.render(root_dir, options.skip_chmod, options.skip_chown)

    def _clone(self, argv):
        if len(argv) != 3:
            raise MissingException("This action takes 3 arguments")

        host = self._get_resource(argv)
        host.clone()

    def _changes(self, argv):
        if len(argv) != 3:
            raise MissingException("This action takes 3 arguments")

        host = self._get_resource(argv)
        changes = host.get_changes()
        print "Changes:"
        for c in changes:
            c.show()

    def _provision(self, argv):
        host = self._get_resource(argv)
        host.provision()

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <env_name>
                       List all hosts, optionally within an environment
    show <org_name> <env_name> <host_name>
                       Show the details of a host
    applications <...>
                       Application contexts handling
    settings <...>
                       Settings handling
    instance <...>
                       Instance handling
    changes <org_name> <env_name> <host_name>
                       Show pending changes
    render-file <org_name> <env_name> <host_name> <app_name> <file_name>
                       Renders a file of a given application
    render-ks <org_name> <env_name> <host_name>
                       Renders kickstart
    render-tree <org_name> <env_name> <host_name> <output directory>
    [--skip-chown] [--skip-chmod]
                    Outputs all files associated to a particular host to a
                    given directory. Note that if a file c has path /a/b/c and
                    output directory's path is /d/e/, the file will be written
                    to /d/e/a/b/c. File c will have proper permissions and
                    ownership unless it is asked not to do so (--skip-chown
                    and --skip-chmod flags).
    add <org_name> <env_name>
                       Add an host
    update <org_name> <env_name> <host_name>
                       Update a host
    delete <org_name> <env_name> <host_name>
                       Delete a host
'''
