# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.abstract import AbstractController
from cortex_client.control.doc import ActionDoc
from cortex_client.api.sync import SyncEngine
from cortex_client.control import completions
from cortex_client.control.exceptions import ArgumentException
from cortex_client.api import collections
from cortex_client.util import globals

class SyncController(AbstractController):

    def __init__(self, doc_params):
        super(SyncController, self).__init__()
        self._doc = "Sync."
        self._doc_params = doc_params

        self._register(["pull"], self._pull, self._print_sync_completions)
        self._register(["push"], self._push, self._print_sync_completions)
        self._register(["help"], self._help)
        self._default_action = self._help

        self._register_action_doc(self._pull_doc())

    def _print_sync_completions(self, argv):
        pass

    def _get_resource_and_folder(self, argv):
        return (None, None)

    def _help(self, argv):
        self._print_doc()

    def _pull(self, argv):
        (remote_res, folder) = self._get_resource_and_folder(argv)
        sync = SyncEngine(folder)

        sync.pull(remote_res, globals.options.dry_run)

    def _pull_doc(self):
        return ActionDoc("pull", self._doc_params, """
        Pulls changes from remote resource and updates local files.""")

    def _push(self, argv):
        (remote_res, folder) = self._get_resource_and_folder(argv)
        sync = SyncEngine(folder)

        sync.push(remote_res, globals.options.dry_run)

    def _push_doc(self):
        return ActionDoc("push", self._doc_params, """
        Push changes from local resource to server.""")

class AppSyncController(SyncController):
    def __init__(self):
        super(AppSyncController, self).__init__("<org_name> <app_name> <local_folder>")

    def _print_sync_completions(self, param_num, argv):
        completions.app_sync_completions(self._api, param_num, argv)

    def _get_resource_and_folder(self, argv):
        if len(argv) != 3:
            raise ArgumentException("Expected org name, app name and folder path")
        res = collections.applications(self._api, argv[0]).get_resource(argv[1])
        return (res, argv[2])
