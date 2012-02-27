# coding: utf-8

import json

from cortex_client.util import prompt, globals
from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException
from cortex_client.control.doc import ActionDoc

class InstancesController(ResourceController):

    def __init__(self):
        super(InstancesController, self).__init__()

        # actions
        self._register(["start"], self._start, self._print_resource_completions)
        self._register(["pause"], self._pause, self._print_resource_completions)
        self._register(["resume"], self._resume, self._print_resource_completions)
        self._register(["shutdown"], self._shutdown, self._print_resource_completions)
        self._register(["poweroff"], self._poweroff, self._print_resource_completions)
        self._register(["properties"], self._properties, self._print_resource_completions)

        # Unregister unsupported actions
        self._unregister(["update", "list", "add"])

        self._doc = "Host instances handling."
        self._update_action_doc_params("delete", "<org_name>  <env_name> <host_name>")
        self._update_action_doc_params("show", "<org_name>  <env_name> <host_name>")
        self._register_action_doc(self._start_doc())
        self._register_action_doc(self._pause_doc())
        self._register_action_doc(self._resume_doc())
        self._register_action_doc(self._shutdown_doc())
        self._register_action_doc(self._poweroff_doc())
        self._register_action_doc(self._properties_doc())

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])

        return host.instance()

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.environments())
        elif len(argv) > 1 and param_num == 2:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            self._print_identifiers(env.hosts())

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        else:
            print ""

    def _get_name_argument(self, argv):
        return ""

    def _properties(self, argv):
        instance = self._get_resource(argv)
        options = globals.options
        if options.raw:
            print json.dumps(instance._get_field("properties"), indent = 4)
        else:
            props = instance.get_properties()
            for p in props:
                p.show()

    def _properties_doc(self):
        return ActionDoc("properties", "<org_name>  <env_name> <host_name>", """
        Show properties of a given host instance.""")

    def _delete(self, argv):
        instance = self._get_resource(argv)
        if prompt.confirm(prompt = "Delete VM ?", resp = False):
            instance.delete()

    def _delete_doc(self):
        return ActionDoc("delete", "<org_name>  <env_name> <host_name>", """
        Delete a host instance.""")

    def _start(self, argv):
        instance = self._get_resource(argv)
        instance.start()

    def _start_doc(self):
        return ActionDoc("start", "<org_name>  <env_name> <host_name>", """
        Start a host instance.""")

    def _pause(self, argv):
        instance = self._get_resource(argv)
        instance.pause()

    def _pause_doc(self):
        return ActionDoc("pause", "<org_name>  <env_name> <host_name>", """
        Pause a host instance.""")

    def _resume(self, argv):
        instance = self._get_resource(argv)
        instance.resume()

    def _resume_doc(self):
        return ActionDoc("resume", "<org_name>  <env_name> <host_name>", """
        Resume a host instance.""")

    def _shutdown(self, argv):
        instance = self._get_resource(argv)
        instance.shutdown()

    def _shutdown_doc(self):
        return ActionDoc("shutdown", "<org_name>  <env_name> <host_name>", """
        Shutdown a host instance.""")

    def _poweroff(self, argv):
        instance = self._get_resource(argv)
        instance.poweroff()

    def _poweroff_doc(self):
        return ActionDoc("poweroff", "<org_name>  <env_name> <host_name>", """
        Power-off a host instance.""")
