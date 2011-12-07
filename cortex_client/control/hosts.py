# control.hosts - Controller for cortex Hosts resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.util import prompt
from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import ArgumentException
from cortex_client.api.exceptions import PythonApiException

class HostsController(ResourceController):

    _template = "host.json"

    def __init__(self):
        super(HostsController, self).__init__()
        self._register(["provision"], self._provision, self._print_show_completions)
        self._register(["start"], self._start, self._print_show_completions)
        self._register(["pause"], self._pause, self._print_show_completions)
        self._register(["resume"], self._resume, self._print_show_completions)
        self._register(["shutdown"], self._shutdown, self._print_show_completions)
        self._register(["poweroff"], self._poweroff, self._print_show_completions)
        self._register(["settings"], self._settings, self._print_show_completions)
        self._register(["properties"], self._properties, self._print_show_completions)
        self._register(["instance"], self._instance, self._print_show_completions)

    def get_collection(self, argv):
        if len(argv) < 2:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        return env.hosts()

    def _get_name_argument(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        return argv[2]

    def _settings(self, argv):
        host = self._get_resource(argv)
        host.show_settings()

    def _properties(self, argv):
        host = self._get_resource(argv)
        host.show_properties()

    def _delete(self, argv):
        host = self._get_resource(argv)

        if (prompt.confirm(prompt = "Delete " + host.get_name() + " ?", resp = False)) :
            delete_vm = prompt.confirm(prompt = "Delete VM also ?", resp = False)
            host.delete(delete_vm)

    def _provision(self, argv):
        host = self._get_resource(argv)
        host.provision()

    def _start(self, argv):
        host = self._get_resource(argv)
        host.start()

    def _pause(self, argv):
        host = self._get_resource(argv)
        host.pause()

    def _resume(self, argv):
        host = self._get_resource(argv)
        host.resume()

    def _shutdown(self, argv):
        host = self._get_resource(argv)
        host.shutdown()

    def _poweroff(self, argv):
        host = self._get_resource(argv)
        host.poweroff()

    def _instance(self, argv):
        host = self._get_resource(argv)
        try:
            info = host.get_instance()
            info.show()
        except PythonApiException, e:
            print e.message

    def _help(self, argv):
        print '''You must provide an action to perform on this resource.

Actions:
    list <org_name> <env_name>
                       List all hosts, optionally within an environment
    show <org_name> <env_name> <host_name>
                       Show the details of a host
    settings <org_name> <env_name> <host_name>
                       Show the settings of a host
    instance <org_name> <env_name> <host_name>
                       Show information about host's instance (including IP
                       address and hostname if available)
    add <org_name> <env_name>
                       Add an host
    update <org_name> <env_name> <host_name>
                       Update a host
    delete <org_name> <env_name> <host_name>
                       Delete a host
    provision <org_name> <env_name> <host_name>
                       Provision a host
    start <org_name> <env_name> <host_name>
                       Start a host
    pause <org_name> <env_name> <host_name>
                       Pause a host
    resume <org_name> <env_name> <host_name>
                       Resume a host's execution
    shutdown <org_name> <env_name> <host_name>
                       Shutdown a host
    poweroff <org_name> <env_name> <host_name>
                       Power-off a host
'''
