# coding: utf-8

import os

from cortex_client.util import path
from cortex_client.api.exceptions import PythonApiException
from cortex_client.api.collection import ResourceNotFoundException

class ExportException(Exception):
    pass

class Export(object):
    def __init__(self, force = False):
        self._force = force

    def _export_resource(self, res, res_folder):
        # Ensures local repository does not contain stale data
        if(os.path.exists(res_folder) and len(os.listdir(res_folder)) > 0) and not self._force:
            raise ExportException(res_folder + " already exists and is not empty.")

        res.dump(res_folder)

    def _export_files_content(self, resource, output_folder):
        for template in resource.files().get_resources():
            file_name = template.get_name()
            with open(os.path.join(output_folder, file_name), "w") as f:
                f.write(template.get_content().read())

    def _export_resource_with_files(self, res, res_folder):
        self._export_resource(res, res_folder)

        # Dump files' content to disk
        files_folder = os.path.join(res_folder, "files")
        path.ensure(files_folder)
        self._export_files_content(res, files_folder)

    def export_application(self, app, app_folder):
        self._export_resource_with_files(app, app_folder)

    def export_distribution(self, dist, dist_folder):
        self._export_resource_with_files(dist, dist_folder)

    def export_platform(self, plat, plat_folder):
        self._export_resource_with_files(plat, plat_folder)

    def export_environment(self, env, env_folder):
        self._export_resource(env, env_folder)

        hosts_folder = os.path.join(env_folder, "hosts")
        for host in env.hosts().get_resources():
            self.export_host(host, os.path.join(hosts_folder, host.get_name()))

    def export_host(self, host, host_folder):
        self._export_resource(host, host_folder)

        # Export instance
        try:
            instance = host.instance().get_single_resource()
            instance.dump_json(os.path.join(host_folder, "instance.json"))
        except PythonApiException:
            pass

        # Export application contexts
        app_contexts = host.applications().get_resources()
        app_folder = os.path.join(host_folder, "applications")
        path.ensure(app_folder)
        for context in app_contexts:
            context.dump_json(os.path.join(app_folder, context.get_application() + ".json"))

        # Export platform context
        try:
            context = host.platform().get_single_resource()
            context.dump_json(os.path.join(host_folder, "platform.json"))
        except ResourceNotFoundException:
            pass

        # Export distribution context
        try:
            context = host.distribution().get_single_resource()
            context.dump_json(os.path.join(host_folder, "distribution.json"))
        except ResourceNotFoundException:
            pass

    def export_organization(self, org, org_folder):
        self._export_resource(org, org_folder)

        for app in org.applications().get_resources():
            self.export_application(app, os.path.join(org_folder, "applications", app.get_name()))
        for dist in org.distributions().get_resources():
            self.export_distribution(dist, os.path.join(org_folder, "distributions", dist.get_name()))
        for plat in org.platforms().get_resources():
            self.export_platform(plat, os.path.join(org_folder, "platforms", plat.get_name()))
        for env in org.environments().get_resources():
            self.export_environment(env, os.path.join(org_folder, "environments", env.get_name()))
