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

    def export_application(self, app, app_folder):
        # Ensures local repository does not contain stale data
        if(os.path.exists(app_folder) and len(os.listdir(app_folder)) > 0) and not self._force:
            raise ExportException(app_folder + " already exists and is not empty.")

        app.dump(app_folder)

        # Dump files' content to disk
        files_folder = os.path.join(app_folder, "files")
        path.ensure(files_folder)
        self._export_files_content(app, files_folder)
