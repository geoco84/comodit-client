# coding: utf-8

import os

from cortex_client.api.application import Application
from cortex_client.api.collection import ResourceNotFoundException
from cortex_client.api.distribution import Distribution
from cortex_client.api.platform import Platform

class ImportException(Exception):
    pass

class Import(object):
    def __init__(self, force_update = False):
        self._force_update = force_update

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

        if remote_res != None:
            remote_uuid = remote_res.get_uuid()
            if(remote_uuid == local_uuid):
                local_res.commit()
            else:
                raise ImportException("There is a conflict for resource " + res_name)
        else:
            local_res.create()

    def _import_file_content(self, src_file, app, name):
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
