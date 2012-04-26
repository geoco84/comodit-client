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
    def __init__(self, skip_existing = False, queue_actions = False):
        self._skip_existing = skip_existing
        self._queue_actions = queue_actions
        self._actions_queue = ActionsQueue()

    def _import_resource(self, local_res):
        res_name = local_res.get_name()

        # Retrieve remote resource (if it exists)
        collection = local_res.get_collection()
        try:
            collection.get_resource(res_name)
            if not self._skip_existing and not self._queue_actions:
                raise ImportException("There is a conflict for resource " + res_name)
            elif self._queue_actions:
                self._actions_queue.add_action(CreateResource(True, local_res))
        except ResourceNotFoundException:
            if self._queue_actions:
                self._actions_queue.add_action(CreateResource(False, local_res))
            else:
                local_res.create()

    def _import_instance(self, instance):
        try:
            instance.get_collection().get_single_resource()
        except PythonApiException:
            if self._queue_actions:
                self._actions_queue.add_action(CreateInstance(instance))
            else:
                instance.create()

    def _import_file_content(self, src_file, app, name):
        if self._queue_actions:
            self._actions_queue.add_action(UploadContent(src_file, app, name))
        else:
            app.files().get_resource(name).set_content(src_file)

    def _import_resource_with_files(self, res, root_folder):
        res.load(root_folder)

        self._import_resource(res)

        # Push files' content
        file_list = res.get_files()
        for f in file_list:
            file_name = f.get_name()
            content_file = os.path.join(root_folder, "files", file_name)
            self._import_file_content(content_file, res, file_name)

    def import_application(self, org, root_folder):
        app = Application(org.applications(), None)
        self._import_resource_with_files(app, root_folder)

    def import_distribution(self, org, root_folder):
        dist = Distribution(org.distributions(), None)
        self._import_resource_with_files(dist, root_folder)

    def import_platform(self, org, root_folder):
        plat = Platform(org.platforms(), None)
        self._import_resource_with_files(plat, root_folder)

    def import_environment(self, org, env_folder):
        env = Environment(org.environments(), None)
        env.load(env_folder)
        self._import_resource(env)

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

        self._import_resource(host)

        # Import application contexts
        for app in apps:
            context = ApplicationContext(host.applications(), None)
            context.load_json(os.path.join(host_folder, "applications", app + ".json"))
            self._import_resource(context)

        # Import platform context
        platform_file = os.path.join(host_folder, "platform.json")
        if os.path.exists(platform_file):
            context = PlatformContext(host.platform(), None)
            context.load_json(platform_file)
            self._import_resource(context)

        # Import distribution context
        dist_file = os.path.join(host_folder, "distribution.json")
        if os.path.exists(dist_file):
            context = DistributionContext(host.distribution(), None)
            context.load_json(dist_file)
            self._import_resource(context)

        # Import instance (must come at last)
        instance_file = os.path.join(host_folder, "instance.json")
        if os.path.exists(instance_file):
            instance = Instance(host.instance(), None)
            instance.load_json(instance_file)
            self._import_instance(instance)

    def import_organization(self, api, org_folder):
        org = Organization(api.organizations(), None)
        org.load(org_folder)

        self._import_resource(org)

        for app in os.listdir(os.path.join(org_folder, "applications")):
            self.import_application(org, os.path.join(org_folder, "applications", app))

        for dist in os.listdir(os.path.join(org_folder, "distributions")):
            self.import_distribution(org, os.path.join(org_folder, "distributions", dist))

        for plat in os.listdir(os.path.join(org_folder, "platforms")):
            self.import_platform(org, os.path.join(org_folder, "platforms", plat))

        for env in os.listdir(os.path.join(org_folder, "environments")):
            self.import_environment(org, os.path.join(org_folder, "environments", env))

    def display_queue(self):
        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        self._actions_queue.display_actions()

    def execute_queue(self):
        if not self._queue_actions:
            raise ImportException("Queueing is not enabled")

        self._actions_queue.apply_actions(self._skip_existing)

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
    def __init__(self, src_file, res, file_name):
        super(UploadContent, self).__init__(False)
        self._src_file = src_file
        self._res = res
        self._file_name = file_name

    def get_summary(self):
        return "Upload file " + self._src_file

    def execute(self):
        file_res = self._res.files().get_resource(self._file_name)
        file_res.set_content(self._src_file)

class ResourceAction(Action):
    def __init__(self, is_fast_forward, res_object):
        super(ResourceAction, self).__init__(is_fast_forward)
        self._res_object = res_object

    def display(self):
        super(ResourceAction, self).display()
        print "Resource:", self._res_object.__class__.__name__

class CreateResource(ResourceAction):
    def __init__(self, is_fast_forward, res_object):
        super(CreateResource, self).__init__(is_fast_forward, res_object)

    def execute(self):
        self._res_object.create()

    def get_summary(self):
        return "Create resource " + self._res_object.get_name()

class CreateInstance(CreateResource):
    def __init__(self, instance):
        super(CreateInstance, self).__init__(False, instance)

    def get_summary(self):
        return "Create instance for host " + self._res_object.get_host()

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

    def apply_actions(self, skip_existing):
        for a in self._actions:
            if not a.conflict():
                print "-"*80
                print "Executing '" + a.get_summary() + "'"
                try:
                    a.execute()
                except Exception, e:
                    print "Error:", e.message
        print "-"*80

    def display_actions(self):
        for a in self._actions:
            print "-"*80
            a.display()
        print "-"*80
