# control.organizations - Controller for cortex Organizations resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import os, json

from cortex_client.util import globals
from cortex_client.control.root_resource import RootResourceController
from cortex_client.control.exceptions import ArgumentException, \
    ControllerException
from cortex_client.control.settings import OrganizationSettingsController
from cortex_client.control.groups import GroupsController
from cortex_client.control.doc import ActionDoc
from cortex_client.api import collections
from cortex_client.control.audit import AuditHelper
from cortex_client.api.exporter import Export
from cortex_client.api.importer import Import


class SyncException(ControllerException):
    def __init__(self, msg):
        ControllerException.__init__(self, msg)


class OrganizationsController(RootResourceController):

    _template = "organization.json"

    def __init__(self):
        super(OrganizationsController, self).__init__()
        self._audit = AuditHelper(self, "<res_name>")

        # actions
        self._register(["import"], self._import, self._print_import_completions)
        self._register(["export"], self._export, self._print_export_completions)
        self._register(["reset-secret"], self._reset_secret, self._print_resource_completions)
        self._register(["audit"], self._audit.audit, self._print_resource_completions)

        self._register_action_doc(self._export_doc())
        self._register_action_doc(self._import_doc())
        self._register_action_doc(self._reset_secret_doc())
        self._register_action_doc(self._audit.audit_doc())

        # subcontrollers
        self._register_subcontroller(["settings"], OrganizationSettingsController())
        self._register_subcontroller(["groups"], GroupsController())

        self._doc = "Organizations handling."

    def get_collection(self, argv):
        return self._api.organizations()

    def _prune_json_update(self, json_wrapper):
        super(OrganizationsController, self)._prune_json_update(json_wrapper)
        json_wrapper._del_field("settings")
        json_wrapper._del_field("groups")
        json_wrapper._del_field("environments")

    def _print_group_completions(self, param_num, argv):
        if param_num < 1:
            self._print_resource_completions(param_num, argv)
        elif param_num == 1:
            self._print_identifiers(collections.groups(self._api, argv[0]))

    def _show_group(self, argv):
        if len(argv) != 2:
            raise ArgumentException("This action takes 2 arguments")

        group = collections.groups(self._api, argv[0]).get_resource(argv[1])
        group.show()

    def _add_user(self, argv):
        if len(argv) != 3:
            raise ArgumentException("This action takes 3 arguments")

        group = collections.groups(self._api, argv[0]).get_resource(argv[1])
        group.add_user(argv[2])
        group.commit()

    def _del_user(self, argv):
        if len(argv) != 3:
            raise ArgumentException("This action takes 3 arguments")

        group = collections.groups(self._api, argv[0]).get_resource(argv[1])
        group.remove_user(argv[2])
        group.commit()

    def _reset_secret(self, argv):
        org = self._get_resource(argv)
        org.reset_secret()

    def _reset_secret_doc(self):
        return ActionDoc("reset-secret", self._list_params(), """
        Resets the secret key associated to the organization.""")

    def _audit(self, argv):
        org = self._get_resource(argv)
        logs = org.audit_logs().get_resources()

        # Display the result
        options = globals.options
        if options.raw:
            json.dumps(logs, sort_keys = True, indent = 4)
        else:
            for log in logs:
                print log.get_timestamp(), log.get_message(), "by", log.get_initiator()

    def _audit_doc(self):
        return ActionDoc("audit", self._list_params(), """
        Displays audit log.""")

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

        org = self._api.organizations().get_resource(argv[0])
        export = Export(globals.options.force)
        export.export_organization(org, self._root)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> [<output_folder>] [--force]", """
        Export organization onto disk. --force option causes existing files to
        be overwritten.""")

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

        if len(argv) < 1:
            raise ArgumentException("Wrong number of arguments")
        self._root = argv[0]

        importer = Import(globals.options.skip_existing)
        importer.import_organization(self._api, self._root)

    def _import_doc(self):
        return ActionDoc("import", "<src_folder>] [--force]", """
        Import organization from disk. --force option causes existing resources
        on server to be updated.""")
