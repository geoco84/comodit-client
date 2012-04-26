# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.api import collections

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.settings import PlatformSettingsController
from cortex_client.control.files import PlatformFilesController
from cortex_client.control.parameters import PlatformParametersController
from cortex_client.api.exporter import Export
from cortex_client.util import globals
from cortex_client.control.doc import ActionDoc

class PlatformsController(OrganizationResourceController):

    _template = "platform.json"

    def __init__(self):
        super(PlatformsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], PlatformSettingsController())
        self._register_subcontroller(["files"], PlatformFilesController())
        self._register_subcontroller(["parameters"], PlatformParametersController())

        self._doc = "Platforms handling."

        # actions
        self._register(["export"], self._export, self._print_export_completions)

        self._register_action_doc(self._export_doc())

    def _get_collection(self, org_name):
        return collections.platforms(self._api, org_name)

    def _prune_json_update(self, json_wrapper):
        super(PlatformsController, self)._prune_json_update(json_wrapper)
        json_wrapper._del_field("organization")
        json_wrapper._del_field("settings")
        json_wrapper._del_field("files")
        json_wrapper._del_field("parameters")

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

        export = Export(globals.options)
        export.export_application(app, root_folder)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> <app_name> [<output_folder>] [--force]", """
        Export application onto disk. --force option causes existing files to
        be overwritten.""")
