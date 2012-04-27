# coding: utf-8

import os, json

from cortex_client.api.application import Application
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.distribution import Distribution
from cortex_client.api.platform import Platform
from cortex_client.api.environment import Environment
from cortex_client.api.host import Host, Instance
from cortex_client.api.contexts import ApplicationContext, PlatformContext, \
    DistributionContext
from cortex_client.api.organization import Organization
from cortex_client.api.exceptions import PythonApiException

class ImportException(Exception):
    pass

class Import(object):
    def __init__(self, skip_conflict = False, queue_actions = False):
        self._skip_conflict = skip_conflict
        self._queue_actions = queue_actions
        self._actions_queue = ActionsQueue()

    def _import_resource(self, local_res, resource_type = "resource"):
        res_name = local_res.get_name()

        # Retrieve remote resource (if it exists)
        collection = local_res.get_collection()
        try:
            collection.get_resource(res_name)
            if not self._skip_conflict and not self._queue_actions:
                raise ImportException("There is a conflict for " + resource_type + " '" + res_name + "'")
            elif self._queue_actions:
                self._actions_queue.add_action(CreateResource(True, local_res, resource_type))
        except ResourceNotFoundException:
            if self._queue_actions:
                self._actions_queue.add_action(CreateResource(False, local_res, resource_type))
            else:
                local_res.create()

    def _import_instance(self, instance):
        try:
            instance.get_collection().get_single_resource()
        except PythonApiException:
            if self._queue_actions:
                self._actions_queue.add_action(CreateResource(False, instance, "host instance"))
            else:
                instance.create()

    def _import_file_content(self, src_file, app, name, resource_type = "resource"):
        if self._queue_actions:
            self._actions_queue.add_action(UploadContent(src_file, app, name, resource_type))
        else:
            app.files().get_resource(name).set_content(src_file)

    def _import_resource_with_files(self, res, root_folder, resource_type = "resource"):
        res.load(root_folder)

        self._import_resource(res, resource_type)

        # Push files' content
        file_list = res.get_files()
        for f in file_list:
            file_name = f.get_name()
            content_file = os.path.join(root_folder, "files", file_name)
            self._import_file_content(content_file, res, file_name, resource_type)

    def import_application(self, org, root_folder):
        app = Application(org.applications(), None)
        self._import_resource_with_files(app, root_folder, "application")

    def import_distribution(self, org, root_folder):
        dist = Distribution(org.distributions(), None)
        self._import_resource_with_files(dist, root_folder, "distribution")

    def import_platform(self, org, root_folder):
        plat = Platform(org.platforms(), None)
        self._import_resource_with_files(plat, root_folder, "platform")

    def import_environment(self, org, env_folder):
        env = Environment(org.environments(), None)
        env.load(env_folder)
        self._import_resource(env, "environment")

        # Push hosts
        hosts_folder = os.path.join(env_folder, "hosts")
        hosts_list = os.listdir(hosts_folder)
        for host_name in hosts_list:
            host_folder = os.path.join(hosts_folder, host_name)

            self.import_host(env, host_folder)

    def import_host(self, env, host_folder):
        host = Host(env.hosts(), None)
        host.load(host_folder)

        apps = host.get_applications()

        # Contexts are created below
        host._del_field("applications")
        host._del_field("platform")
        host._del_field("distribution")

        self._import_resource(host, "host")

        # Import application contexts
        for app in apps:
            context = ApplicationContext(host.applications(), None)
            context.load_json(os.path.join(host_folder, "applications", app + ".json"))
            self._import_resource(context, "application context")

        # Import platform context
        platform_file = os.path.join(host_folder, "platform.json")
        if os.path.exists(platform_file):
            context = PlatformContext(host.platform(), None)
            context.load_json(platform_file)
            self._import_resource(context, "platform context")

        # Import distribution context
        dist_file = os.path.join(host_folder, "distribution.json")
        if os.path.exists(dist_file):
            context = DistributionContext(host.distribution(), None)
            context.load_json(dist_file)
            self._import_resource(context, "distribution context")

        # Import instance (must come at last)
        instance_file = os.path.join(host_folder, "instance.json")
        if os.path.exists(instance_file):
            instance = Instance(host.instance(), None)
            instance.load_json(instance_file)
            self._import_instance(instance)

    def import_organization(self, api, org_folder):
        org = Organization(api.organizations(), None)
        org.load(org_folder)

        self._import_resource(org, "organization")

        for app in os.listdir(os.path.join(org_folder, "applications")):
            self.import_application(org, os.path.join(org_folder, "applications", app))

        for dist in os.listdir(os.path.join(org_folder, "distributions")):
            self.import_distribution(org, os.path.join(org_folder, "distributions", dist))

        for plat in os.listdir(os.path.join(org_folder, "platforms")):
            self.import_platform(org, os.path.join(org_folder, "platforms", plat))

        for env in os.listdir(os.path.join(org_folder, "environments")):
            self.import_environment(org, os.path.join(org_folder, "environments", env))

    def display_queue(self, show_only_conflicts = True):
        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        self._actions_queue.display_actions(show_only_conflicts)

    def execute_queue(self):
        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        self._actions_queue.apply_actions(self._skip_conflict)

    def no_conflict(self):
        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        return self._actions_queue.no_conflict()

class Action(object):
    def __init__(self, conflict):
        self._conflict = conflict

    def conflict(self):
        return self._conflict

    def execute(self):
        raise NotImplementedError

    def get_summary(self):
        raise NotImplementedError

    def display(self):
        print "Conflict:", self._conflict
        print "Summary: " + self.get_summary()

class UploadContent(Action):
    def __init__(self, src_file, res, file_name, resource_type = "resource"):
        super(UploadContent, self).__init__(False)
        self._src_file = src_file
        self._res = res
        self._resource_type = resource_type
        self._file_name = file_name

    def get_summary(self):
        return "Upload file " + self._src_file + " to " + self._resource_type + " '" + self._res.get_name() + "'"

    def execute(self):
        file_res = self._res.files().get_resource(self._file_name)
        file_res.set_content(self._src_file)

class CreateResource(Action):
    def __init__(self, conflict, res_object, resource_type):
        super(CreateResource, self).__init__(conflict)
        self._res_object = res_object
        self._resource_type = resource_type

    def execute(self):
        self._res_object.create()

    def get_summary(self):
        return "Create " + self._resource_type + " '" + self._res_object.get_name() + "'"

class ActionsQueue:
    def __init__(self):
        self._no_conflict = True
        self._actions = []

    def add_action(self, action):
        if action.conflict():
            self._no_conflict = False
        self._actions.append(action)

    def no_conflict(self):
        return self._no_conflict

    def apply_actions(self, skip_conflicts):
        if not self._no_conflict and not skip_conflicts:
            raise ImportException("Cannot apply actions, conflicts detected")

        for a in self._actions:
            print "-"*80
            if not a.conflict():
                print "Executing '" + a.get_summary() + "'"
                try:
                    a.execute()
                except Exception, e:
                    print "Error:", e.message
            else:
                print "Skipping '" + a.get_summary() + "'"
        print "-"*80

    def display_actions(self, show_only_conflicts):
        for a in self._actions:
            if not show_only_conflicts or a.conflict():
                print "-"*80
                a.display()
        print "-"*80
