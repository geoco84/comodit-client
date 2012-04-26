# control.distributions - Controller for cortex Distributions resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.api import collections

from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.settings import DistributionSettingsController
from cortex_client.control.files import DistributionFilesController
from cortex_client.control.parameters import DistributionParametersController
from cortex_client.api.exporter import Export
from cortex_client.util import globals
from cortex_client.control.doc import ActionDoc
from cortex_client.control.exceptions import ArgumentException
from cortex_client.api.importer import Import

class DistributionsController(OrganizationResourceController):

    _template = "distribution.json"

    def __init__(self):
        super(DistributionsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], DistributionSettingsController())
        self._register_subcontroller(["files"], DistributionFilesController())
        self._register_subcontroller(["parameters"], DistributionParametersController())

        self._doc = "Distributions handling."

        # actions
        self._register(["import"], self._import, self._print_import_completions)
        self._register(["export"], self._export, self._print_export_completions)

        self._register_action_doc(self._export_doc())
        self._register_action_doc(self._import_doc())

    def _get_collection(self, org_name):
        return collections.distributions(self._api, org_name)

    def _prune_json_update(self, json_wrapper):
        super(DistributionsController, self)._prune_json_update(json_wrapper)
        json_wrapper._del_field("organization")
        json_wrapper._del_field("settings")
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

        export = Export(globals.options)
        export.export_application(app, root_folder)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> <dist_name> [<output_folder>] [--force]", """
        Export distribution onto disk. --force option causes existing files to
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
        imp = Import(globals.options)
        imp.import_distribution(org, argv[1])

    def _import_doc(self):
        return ActionDoc("import", "<org_name> <src_folder> [--force]", """
        Import distribution from disk. --force option causes existing resources
        on server to be updated.""")
