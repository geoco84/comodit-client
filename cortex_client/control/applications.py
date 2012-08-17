# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import json, os

from cortex_client.api import collections
from cortex_client.api.exporter import Export
from cortex_client.api.importer import Import
from cortex_client.util import globals
from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.files import ApplicationFilesController
from cortex_client.control.parameters import ApplicationParametersController
from cortex_client.control.doc import ActionDoc
from cortex_client.control.exceptions import ArgumentException
from cortex_client.api.exceptions import PythonApiException
from cortex_client.config import Config
from cortex_client.util.editor import edit_text

class ApplicationsController(OrganizationResourceController):

    _template = "application.json"

    def __init__(self):
        super(ApplicationsController, self).__init__()

        # sub-controllers
        self._register_subcontroller(["files"], ApplicationFilesController())
        self._register_subcontroller(["parameters"], ApplicationParametersController())

        self._doc = "Applications handling."

        # actions
        self._register(["import"], self._import, self._print_import_completions)
        self._register(["export"], self._export, self._print_export_completions)
        self._register(["publish"], self._publish, self._print_resource_completions)
        self._register(["unpublish"], self._unpublish, self._print_resource_completions)
        self._register(["push"], self._push, self._print_resource_completions)

        self._register_action_doc(self._export_doc())
        self._register_action_doc(self._import_doc())
        self._register_action_doc(self._publish_doc())
        self._register_action_doc(self._unpublish_doc())
        self._register_action_doc(self._push_doc())

    def _get_collection(self, org_name):
        return collections.applications(self._api, org_name)

    def _prune_json_update(self, json_wrapper):
        super(ApplicationsController, self)._prune_json_update(json_wrapper)
        json_wrapper._del_field("organization")
        json_wrapper._del_field("files")
        json_wrapper._del_field("parameters")

    # Export

    def _print_export_completions(self, param_num, argv):
        if param_num < 2:
            self._print_resource_completions(param_num, argv)
        elif param_num == 2:
            self._print_dir_completions()

    def _export(self, argv):
        self._options = globals.options

        app = self._get_resource(argv)

        root_folder = app.get_name()
        if len(argv) > 2:
            root_folder = argv[2]

        export = Export(globals.options.force)
        export.export_application(app, root_folder)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> <app_name> [<output_folder>] [--force]", """
        Export application onto disk. --force option causes existing files to
        be overwritten.""")

    # Import

    def _print_import_completions(self, param_num, argv):
        if param_num < 1:
            self._print_collection_completions(param_num, argv)
        elif param_num == 1:
            self._print_dir_completions()

    def _import(self, argv):
        if len(argv) != 2:
            raise ArgumentException("Wrong number of arguments")

        org = collections.organizations(self._api).get_resource(argv[0])
        imp = Import()
        imp.import_application(org, argv[1])

    def _import_doc(self):
        return ActionDoc("import", "<org_name> <src_folder> [--skip-existing]", """
        Import application from disk. --skip-existing option causes existing resources
        on server to be updated.""")

    def _publish(self, argv):
        app = self._get_resource(argv)

        if not app.get_published_as() is None:
            raise PythonApiException("Application has already been published")

        template_json = json.load(open(os.path.join(Config()._get_templates_path(), "published_application.json")))
        template_json["application"] = app.get_uuid()
        updated = edit_text(json.dumps(template_json, indent = 4))

        pub_app = self._api.app_store()._new_resource(json.loads(updated))
        self._api.app_store().add_resource(pub_app)

    def _publish_doc(self):
        return ActionDoc("publish", "<org_name> <app_name>", """
        Publish application to store.""")

    def _unpublish(self, argv):
        app = self._get_resource(argv)

        if app.get_published_as() is None:
            raise PythonApiException("Application is not published")

        self._api.app_store().get_resource(app.get_published_as()).delete()

    def _unpublish_doc(self):
        return ActionDoc("unpublish", "<org_name> <app_name>", """
        Unpublish application from store.""")

    def _push(self, argv):
        app = self._get_resource(argv)

        if app.get_published_as() is None:
            raise PythonApiException("Application is not published")

        pub_app = self._api.app_store()._new_resource({"uuid" : app.get_published_as()})
        pub_app.commit()

    def _push_doc(self):
        return ActionDoc("push", "<org_name> <app_name>", """
        Push application update to store.""")
