# coding: utf-8

import os

from cortex_client.util import path

class ExportException(Exception):
    pass

class Export(object):
    def __init__(self, force = False):
        self._force = force

    def _export_files_content(self, resource, output_folder):
        for template in resource.files().get_resources():
            file_name = template.get_name()
            with open(os.path.join(output_folder, file_name), "w") as f:
                f.write(template.get_content().read())

    def _export_resource_with_files(self, res, res_folder):
        # Ensures local repository does not contain stale data
        if(os.path.exists(res_folder) and len(os.listdir(res_folder)) > 0) and not self._force:
            raise ExportException(res_folder + " already exists and is not empty.")

        res.dump(res_folder)

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
