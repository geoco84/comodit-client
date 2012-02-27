# control.organizations - Controller for cortex Organizations resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import os, json

from cortex_client.util import path, globals
from cortex_client.control.root_resource import RootResourceController
from cortex_client.control.exceptions import ArgumentException, \
    ControllerException
from cortex_client.control.settings import OrganizationSettingsController
from cortex_client.control.groups import GroupsController
from cortex_client.control.doc import ActionDoc
from cortex_client.control.actions import ActionsQueue, UploadContent, \
    UpdateResource, CreateResource, CreateInstance
from cortex_client.api.application import Application
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.distribution import Distribution
from cortex_client.api.organization import Organization
from cortex_client.api.group import Group
from cortex_client.api.environment import Environment
from cortex_client.api.host import Host, Instance
from cortex_client.api.platform import Platform


class SyncException(ControllerException):
    def __init__(self, msg):
        ControllerException.__init__(self, msg)


class OrganizationsController(RootResourceController):

    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self).__init__()

        # actions
        self._register(["import"], self._import, self._print_import_completions)
        self._register(["export"], self._export, self._print_export_completions)

        self._register_action_doc(self._export_doc())
        self._register_action_doc(self._import_doc())

        # subcontrollers
        self._register_subcontroller(["settings"], OrganizationSettingsController())
        self._register_subcontroller(["groups"], GroupsController())

        self._doc = "Organizations handling."

    def get_collection(self, argv):
        return self._api.organizations()

    def _print_group_completions(self, param_num, argv):
        if param_num < 1:
            self._print_resource_completions(param_num, argv)
        elif param_num == 1:
            org = self._get_resource(argv)
            self._print_identifiers(org.groups())

    def _show_group(self, argv):
        if len(argv) != 2:
            raise ArgumentException("This action takes 2 arguments")

        org = self._get_resource(argv)

        group = org.groups().get_resource(argv[1])
        group.show()

    def _add_user(self, argv):
        if len(argv) != 3:
            raise ArgumentException("This action takes 3 arguments")

        org = self._get_resource(argv)

        group = org.groups().get_resource(argv[1])
        group.add_user(argv[2])
        group.commit()

    def _del_user(self, argv):
        if len(argv) != 3:
            raise ArgumentException("This action takes 3 arguments")

        org = self._get_resource(argv)

        group = org.groups().get_resource(argv[1])
        group.remove_user(argv[2])
        group.commit()


    # Import/export

    def __set_root_folder(self, argv):
        if len(argv) < 1:
            raise ArgumentException("Wrong number of arguments")

        self._root = argv[0] # By default, use organization name as folder name
        if len(argv) > 1:
            self._root = argv[1]

    def _print_export_completions(self, param_num, argv):
        if param_num == 0:
            self._print_resource_completions(param_num, argv)
        elif param_num == 1:
            self._print_dir_completions()

    def _export(self, argv):
        self._options = globals.options

        self.__set_root_folder(argv)

        # Ensures local repository does not contain stale data
        if(os.path.exists(self._root) and len(os.listdir(self._root)) > 0) and not self._options.force:
            raise SyncException(self._root + " already exists and is not empty.")

        org = self._api.organizations().get_resource(argv[0])
        self._export_organization(org)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> [<output_folder>]", """
        Export organization onto disk.""")

    def _print_import_completions(self, param_num, argv):
        if param_num == 0:
            self._print_dir_completions()

    def _import(self, argv):
        """
        Pushes local data to cortex server. Data may include applications,
        distributions, platforms, organizations, environments and hosts.
        Local data are automatically imported if no collision with remote data
        is detected. In case of collision, 'force' option can be used to still
        import data.
        """
        self._options = globals.options

        self.__set_root_folder(argv)

        self._actions = ActionsQueue()
        self._import_organization()

        if self._actions.isFastForward():
            print "Fast-forward import"
            self._actions.executeActions()
        elif not self._actions.isFastForward() and self._options.force:
            print "Push not fast-forward, forcing"
            self._actions.executeActions()
        else:
            print "Push not fast-forward:"
            self._actions.display()

    def _import_doc(self):
        return ActionDoc("import", "<org_name> [<output_folder>]", """
        Import organization from disk.""")

    def _import_file_content(self, src_file, app, name):
        self._actions.addAction(UploadContent(src_file, app, name))

    def _import_applications(self, org):
        apps_folder = self._get_application_folder()
        if not os.path.exists(apps_folder):
            return

        apps_list = os.listdir(apps_folder)
        for app_name in apps_list:
            app = Application(org.applications(), None)
            app_folder = os.path.join(apps_folder, app_name)
            app.load(app_folder)

            self._import_resource(app)

            # Push files' content
            file_list = app.get_files()
            for f in file_list:
                file_name = f.get_name()
                content_file = os.path.join(app_folder, "files", file_name)
                self._import_file_content(content_file, app, file_name)

    def _import_resource(self, local_res):
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

    def _import_instance(self, host, instance):
        try:
            host.instance().get_single_resource()
            return
        except ResourceNotFoundException:
            self._actions.addAction(CreateInstance(True, host, instance))

    def _export_organization(self, org):
        org.dump(self._root)

        self._export_groups(org)
        self._export_applications(org)
        self._export_distributions(org)
        self._export_platforms(org)
        self._export_environments(org)

    def _export_groups(self, org):
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

    def _export_applications(self, org):
        apps = org.applications().get_resources()
        apps_folder = self._get_application_folder()
        for a in apps:
            app_folder = os.path.join(apps_folder, a.get_name())
            a.dump(app_folder)

            # Dump files' content to disk
            files_folder = os.path.join(app_folder, "files")
            path.ensure(files_folder)
            self.__export_files_content(a, files_folder)

    def _import_distributions(self, org):
        dists_folder = self._get_distribution_folder()
        if not os.path.exists(dists_folder):
            return

        dists_list = os.listdir(dists_folder)
        for dist_name in dists_list:
            dist = Distribution(org.distributions(), None)
            dist_folder = os.path.join(dists_folder, dist_name)
            dist.load(dist_folder)

            self._import_resource(dist)

            # Push files' content
            file_list = dist.get_files()
            for f in file_list:
                file_name = f.get_name()
                content_file = os.path.join(dist_folder, "files", file_name)
                self._import_file_content(content_file, dist, file_name)

    def __export_files_content(self, resource, output_folder):
        for template in resource.files().get_resources():
            file_name = template.get_name()
            with open(os.path.join(output_folder, file_name), "w") as f:
                f.write(template.get_content().read())

    def _export_distributions(self, org):
        dists = org.distributions().get_resources()
        dists_folder = self._get_distribution_folder()
        for d in dists:
            dist_folder = os.path.join(dists_folder, d.get_name())
            d.dump(dist_folder)

            # Dump files' content to disk
            files_folder = os.path.join(dist_folder, "files")
            path.ensure(files_folder)
            self.__export_files_content(d, files_folder)

    def _export_environments(self, org):
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
                    instance = h.instance().get_single_resource()
                    instance_file = self._get_instance_file(host_folder)
                    instance.dump_json(instance_file)
                except Exception, e:
                    print e
                    print e.message
                    pass

    def _import_organization(self):
        # Create unconnected organization
        local_org = Organization(self._api.organizations(), None)
        local_org.load(self._root)

        # Create organization
        self._import_resource(local_org)
        self._import_groups(local_org)

        self._import_applications(local_org)
        self._import_distributions(local_org)
        self._import_platforms(local_org)
        self._import_environments(local_org)

    def _import_groups(self, org):
        groups_folder = self._get_group_folder()
        if not os.path.exists(groups_folder):
            return

        groups_list = os.listdir(groups_folder)
        for group_name in groups_list:
            group = Group(org.groups(), None)
            group_folder = os.path.join(groups_folder, group_name)
            group.load(group_folder)

            self._actions.addAction(UpdateResource(True, group))

    def _import_environments(self, org):
        envs_folder = self._get_environment_folder()
        if not os.path.exists(envs_folder):
            return

        envs_list = os.listdir(envs_folder)
        for env_name in envs_list:
            env = Environment(org.environments(), None)
            env_folder = os.path.join(envs_folder, env_name)
            env.load(env_folder)

            self._import_resource(env)

            # Push hosts
            hosts_list = os.listdir(env_folder)
            for host_name in hosts_list:
                host_dir = os.path.join(env_folder, host_name)

                # Skip files
                if os.path.isfile(host_dir):
                    continue

                host = Host(env.hosts(), None)
                host.load(host_dir)

                # Read instance
                instance_file = self._get_instance_file(host_dir)
                instance = None
                if os.path.exists(instance_file):
                    with open(instance_file, "r") as f:
                        instance = Instance(host.instance(), json.load(f))

                if instance is None:
                    host.clear_state()
                self._import_resource(host)

                if not instance is None:
                    self._import_instance(host, instance)


    def _export_platforms(self, org):
        plats = org.platforms().get_resources()
        plats_folder = self._get_platform_folder()
        for p in plats:
            plat_folder = os.path.join(plats_folder, p.get_name())
            p.dump(plat_folder)

            # Dump files' content to disk
            files_folder = os.path.join(plat_folder, "files")
            path.ensure(files_folder)
            self.__export_files_content(p, files_folder)

    def _import_platforms(self, org):
        plats_folder = self._get_platform_folder()
        if not os.path.exists(plats_folder):
            return

        plats_list = os.listdir(plats_folder)
        for plat_name in plats_list:
            plat = Platform(org.platforms(), None)
            plat_folder = os.path.join(plats_folder, plat_name)
            plat.load(plat_folder)

            self._import_resource(plat)

            # Push files' content
            file_list = plat.get_files()
            for f in file_list:
                file_name = f.get_name()
                content_file = os.path.join(plat_folder, "files", file_name)
                self._import_file_content(content_file, plat, file_name)
