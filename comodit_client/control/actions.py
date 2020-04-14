# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from __future__ import absolute_import
from comodit_client.control.abstract import AbstractController
from comodit_client.control.doc import ActionDoc
from comodit_client.control.exceptions import ArgumentException
from . import completions
import sys


class ActionController(AbstractController):

    def __init__(self):
        super(ActionController, self).__init__()
        self._doc = "Action on deployed host."

        self._register(["run"], self._run, self._print_host_completions)
        self._register(["impact"], self._impact, self._print_orchestration_completions)

        self._register(["help"], self._help)
        self._default_action = self._help

        self._register_action_doc(self._run_doc())
        self._register_action_doc(self._impact_doc())

    def _help(self, argv):
        self._print_doc()

    def _get_host(self, argv):
        return self._client.hosts(argv[0], argv[1]).get(argv[2])

    def _run(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments")

        try:
            time_out = int(self._config.options.timeout)
        except Exception:
            sys.exit("Invalid format for timeout")

        host = self._get_host(argv)
        org = argv[0]
        orch_name = argv[3]

        result = host.run_orchestration(orch_name)


        if self._config.options.wait:
            context = self._client.orchestrationContext(org, orch_name, result["uuid"])
            context.wait_finished(time_out, self._config.options.debug)

    def _print_action_completions(self, param_num, argv):
        if param_num < 4:
            self._print_host_completions(param_num, argv)


    def _print_host_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_entity_identifiers(self._client.organizations().list())
        elif len(argv) > 0 and param_num == 1:
            completions.print_entity_identifiers(self._client.environments(argv[0]).list())
        elif len(argv) > 1 and param_num == 2:
            completions.print_entity_identifiers(self._client.hosts(argv[0], argv[1]).list())
        elif len(argv) > 2 and param_num == 3:
            host = self._get_host(argv)
            completions.print_entity_identifiers(host.get_orchestrations().list())

    def _print_orchestration_completions(self, param_num, argv):
        if param_num == 0:
            completions.print_entity_identifiers(self._client.organizations().list())
        elif len(argv) > 0 and param_num == 1:
            completions.print_entity_identifiers(self._client.orchestrations(argv[0]).list())

    def _impact(self, argv):
        if len(argv) < 2:
            raise ArgumentException("Wrong number of arguments")

        orch_name = argv[1]
        self._client.orchestrations(argv[0]).get(orch_name).show()

    def _impact_doc(self):
        return ActionDoc("impact", "<org_name> <action_name>", """
        get impact action.""")

    def _run_doc(self):
        return ActionDoc("run", "<org_name> <env_name> <host_name> <action_name>", """
        run action on given host.""")

            