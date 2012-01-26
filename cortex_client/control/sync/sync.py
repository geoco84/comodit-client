# control.sync - Clone system state on local filesystem and synchronize
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import os, json

from cortex_client.util import globals, path
from cortex_client.control.abstract import AbstractController
from cortex_client.control.exceptions import ArgumentException

from actions import *
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.group import Group
from cortex_client.api.host import Instance
from cortex_client.api.organization import Organization
from cortex_client.control.sync.exceptions import SyncException
from cortex_client.api.application import Application
from cortex_client.api.distribution import Distribution
from cortex_client.api.environment import Environment
from cortex_client.api.platform import Platform

class SyncController(AbstractController):

    def __init__(self):
        super(SyncController, self).__init__()
        self._register(["pull"], self._pull, self._print_pull_completions)
        self._register(["push"], self._push, self._print_push_completions)
        self._register(["help"], self._help)
        self._default_action = self._help

    def __set_root_folder(self, argv):
        if len(argv) < 1:
            raise ArgumentException("Wrong number of arguments")

        self._root = argv[0] # By default, use organization name as folder name
        if len(argv) > 1:
            self._root = argv[1]

    def _print_pull_completions(self, param_num, argv):
        if param_num == 0:
            self._print_resource_identifiers(self._api.organizations().get_resources())
        elif param_num == 1:
            self._print_dir_completions()

    def _pull(self, argv):
        self._options = globals.options

        self.__set_root_folder(argv)

        # Ensures local repository does not contain stale data
        if(os.path.exists(self._root) and len(os.listdir(self._root)) > 0):
            raise SyncException(self._root + " already exists and is not empty.")

        org = self._api.organizations().get_resource(argv[0])
        self._dump_organization(org)

    def _print_push_completions(self, param_num, argv):
        if param_num == 0:
            self._print_dir_completions()

    def _push(self, argv):
        """
        Pushes local data to cortex server. Data may include applications,
        distributions, platforms, organizations, environments and hosts.
        Local data are automatically pushed if no collision with remote data
        is detected. In case of collision, 'force' option can be used to still
        push data.
        """
        self._options = globals.options

        self.__set_root_folder(argv)

        self._actions = ActionsQueue()
        self._push_organization()

        if self._actions.isFastForward():
            print "Fast-forward push"
            self._actions.executeActions()
        elif not self._actions.isFastForward() and self._options.force:
            print "Push not fast-forward, forcing"
            self._actions.executeActions()
        else:
            print "Push not fast-forward:"
            self._actions.display()

    def _push_file_content(self, src_file, app, name):
        self._actions.addAction(UploadContent(src_file, app, name))

    def _push_applications(self, org):
        apps_folder = self._get_application_folder()
        if not os.path.exists(apps_folder):
            return

        apps_list = os.listdir(apps_folder)
        for app_name in apps_list:
            app = Application(org.applications(), None)
            app_folder = os.path.join(apps_folder, app_name)
            app.load(app_folder)

            self._push_resource(app)

            # Push files' content
            file_list = app.get_files()
            for f in file_list:
                file_name = f.get_name()
                content_file = os.path.join(app_folder, "files", file_name)
                self._push_file_content(content_file, app, file_name)

    def _getUniqueName(self, base_name, names_dict):
        if(not names_dict.has_key(base_name)):
            return base_name

        num = 0
        new_name = base_name + str(num)
        while(names_dict.has_key(new_name)):
            num += 1
            new_name = base_name + str(num)

        return new_name

    def _push_resource(self, local_res):
        res_name = local_res.get_name()
        local_uuid = local_res.get_uuid()

        # Retrieve remote resource (if it exists)
        collection = local_res.get_collection()
        remote_res = None
        try:
            remote_res = collection.get_resource(res_name)
        except ResourceNotFoundException:
            pass

        # In function of remote resource existence, queue an action
        if remote_res != None:
            remote_uuid = remote_res.get_uuid()
            if(remote_uuid == local_uuid):
                self._actions.addAction(UpdateResource(False, local_res))
            else:
                raise SyncException("There is a conflict for resource " + res_name)

#            else:
#                new_name = self._getUniqueName(res_name, collection)
#                local_res.set_name(new_name)
#                self._actions.addAction(CreateResource(False, local_res))
        else:
            self._actions.addAction(CreateResource(True, local_res))

    def _push_instance(self, host, instance):
        try:
            host.get_instance()
            return
        except:
            self._actions.addAction(CreateInstance(True, host, instance))

    def _dump_organization(self, org):
        org.dump(self._root)

        self._dump_groups(org)
        self._dump_applications(org)
        self._dump_distributions(org)
        self._dump_platforms(org)
        self._dump_environments(org)

    def _dump_groups(self, org):
        groups = org.groups().get_resources()
        groups_folder = self._get_group_folder()
        for g in groups:
            group_folder = os.path.join(groups_folder, g.get_name())
            g.dump(group_folder)

    def _get_group_folder(self):
        return os.path.join(self._root, "groups")

    def _get_application_folder(self):
        return os.path.join(self._root, "applications")

    def _get_distribution_folder(self):
        return os.path.join(self._root, "distributions")

    def _get_platform_folder(self):
        return os.path.join(self._root, "platforms")

    def _get_environment_folder(self):
        return os.path.join(self._root, "environments")

    def _get_instance_file(self, host_folder):
        return os.path.join(host_folder, "instance.json")

    def _dump_applications(self, org):
        apps = org.applications().get_resources()
        apps_folder = self._get_application_folder()
        for a in apps:
            app_folder = os.path.join(apps_folder, a.get_name())
            a.dump(app_folder)

            # Dump files' content to disk
            files_folder = os.path.join(app_folder, "files")
            path.ensure(files_folder)
            self.__dump_files_content(a, files_folder)

    def _push_distributions(self, org):
        dists_folder = self._get_distribution_folder()
        if not os.path.exists(dists_folder):
            return

        dists_list = os.listdir(dists_folder)
        for dist_name in dists_list:
            dist = Distribution(org.distributions(), None)
            dist_folder = os.path.join(dists_folder, dist_name)
            dist.load(dist_folder)

            self._push_resource(dist)

            # Push files' content
            file_list = dist.get_files()
            for f in file_list:
                file_name = f.get_name()
                content_file = os.path.join(dist_folder, "files", file_name)
                self._push_file_content(content_file, dist, file_name)

    def __dump_files_content(self, resource, output_folder):
        for template in resource.files().get_resources():
            file_name = template.get_name()
            with open(os.path.join(output_folder, file_name), "w") as f:
                f.write(template.get_content().read())

    def _dump_distributions(self, org):
        dists = org.distributions().get_resources()
        dists_folder = self._get_distribution_folder()
        for d in dists:
            dist_folder = os.path.join(dists_folder, d.get_name())
            d.dump(dist_folder)

            # Dump files' content to disk
            files_folder = os.path.join(dist_folder, "files")
            path.ensure(files_folder)
            self.__dump_files_content(d, files_folder)

    def _dump_environments(self, org):
        envs = org.environments().get_resources()
        envs_folder = self._get_environment_folder()
        for e in envs:
            env_folder = os.path.join(envs_folder, e.get_name())
            e.dump(env_folder)

            # Dump hosts
            hosts = e.hosts().get_resources()
            for h in hosts:
                host_folder = os.path.join(env_folder, h.get_name())
                h.dump(host_folder)

                try:
                    instance = h.get_instance()
                    instance_file = self._get_instance_file(host_folder)
                    instance.dump_json(instance_file)
                except:
                    pass

    def _push_organization(self):
        # Create unconnected organization
        local_org = Organization(self._api.organizations(), None)
        local_org.load(self._root)

        # Create organization
        self._push_resource(local_org)
        self._push_groups(local_org)

        self._push_applications(local_org)
        self._push_distributions(local_org)
        self._push_platforms(local_org)
        self._push_environments(local_org)

    def _push_groups(self, org):
        groups_folder = self._get_group_folder()
        if not os.path.exists(groups_folder):
            return

        groups_list = os.listdir(groups_folder)
        for group_name in groups_list:
            group = Group(org.groups(), None)
            group_folder = os.path.join(groups_folder, group_name)
            group.load(group_folder)

            self._actions.addAction(UpdateResource(True, group))

    def _push_environments(self, org):
        envs_folder = self._get_environment_folder()
        if not os.path.exists(envs_folder):
            return

        envs_list = os.listdir(envs_folder)
        for env_name in envs_list:
            env = Environment(org.environments(), None)
            env_folder = os.path.join(envs_folder, env_name)
            env.load(env_folder)

            self._push_resource(env)

            # Push hosts
            hosts_list = os.listdir(env_folder)
            for host_name in hosts_list:
                host_dir = os.path.join(env_folder, host_name)

                # Skip files
                if os.path.isfile(host_dir):
                    continue

                host = Host(env.hosts(), None)
                host.load(host_dir)

                self._push_resource(host)

                # Push instance
                instance_file = self._get_instance_file(host_dir)
                if os.path.exists(instance_file):
                    with open(instance_file, "r") as f:
                        instance = Instance(json.load(f))
                        self._push_instance(host, instance)

    def _dump_platforms(self, org):
        plats = org.platforms().get_resources()
        plats_folder = self._get_platform_folder()
        for p in plats:
            plat_folder = os.path.join(plats_folder, p.get_name())
            p.dump(plat_folder)

            # Dump files' content to disk
            files_folder = os.path.join(plat_folder, "files")
            path.ensure(files_folder)
            self.__dump_files_content(p, files_folder)

    def _push_platforms(self, org):
        plats_folder = self._get_platform_folder()
        if not os.path.exists(plats_folder):
            return

        plats_list = os.listdir(plats_folder)
        for plat_name in plats_list:
            plat = Platform(org.platforms(), None)
            plat_folder = os.path.join(plats_folder, plat_name)
            plat.load(plat_folder)

            self._push_resource(plat)

            # Push files' content
            file_list = plat.get_files()
            for f in file_list:
                file_name = f.get_name()
                content_file = os.path.join(plat_folder, "files", file_name)
                self._push_file_content(content_file, plat, file_name)

    def _help(self, argv):
        print """You must provide an action to perform.

Actions:
    pull <org_name> [path]         Retrieves data from cortex server (local data
                                   are overwritten)
    push <org_name> [path]         Updates data on cortex server (remote data
                                   may be overwritten if --force option is set)
"""

