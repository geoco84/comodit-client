# coding: utf-8
"""
Host module. Provides classes representing a host, host's properties and host's
settings.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from cortex_client.api.resource import Resource
from cortex_client.rest.exceptions import ApiException
from cortex_client.util.json_wrapper import JsonWrapper, StringFactory
from exceptions import PythonApiException
from cortex_client.api.settings import SettingCollection, SettingFactory

class Property(JsonWrapper):
    """
    A host property. A property is composed of a key and a value.
    """
    def __init__(self, json_data = None):
        super(Property, self).__init__(json_data)

    def get_key(self):
        """
        Provides property's key.
        @return: The key
        @rtype: String
        """
        return self._get_field("key")

    def set_key(self, key):
        """
        Sets property's key.
        @param key: The key
        @type key: String
        """
        return self._set_field("key", key)

    def get_value(self):
        """
        Provides property's key.
        @return: The key
        @rtype: String
        """
        return self._get_field("value")

    def set_value(self, value):
        """
        Sets property's value.
        @param value: The value
        @type value: String
        """
        return self._set_field("value", value)

    def show(self, indent = 0):
        """
        Prints this property's state to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        print " "*indent, "Key:", self.get_key()
        print " "*indent, "Value:", self.get_value()

class PropertyFactory(object):
    """
    Host's property factory.
    
    @see: L{Property}
    @see: L{cortex_client.util.json_wrapper.JsonWrapper._get_list_field}
    """
    def new_object(self, json_data):
        """
        Instantiates a L{Property} object using given state.
        
        @param json_data: A quasi-JSON representation of a Property instance's state.
        @type json_data: String, dict or list
        
        @return: A property
        @rtype: L{Property}
        """
        return Property(json_data)

class Vnc(JsonWrapper):
    def get_hostname(self):
        return self._get_field("host")

    def get_port(self):
        return self._get_field("port")

    def show(self, indent = 0):
        print " "*indent, "hostname:", self.get_hostname()
        print " "*indent, "port:", self.get_port()


class Instance(JsonWrapper):
    """
    Runtime host instance information.
    """

    def get_state(self):
        """
        Provides the state of the instance.
        @return: Instance's state
        @rtype: String
        """
        return self._get_field("state")

    def get_ip(self):
        return self._get_field("ip")

    def get_hostname(self):
        return self._get_field("hostname")

    def get_vnc(self):
        return Vnc(self._get_field("vnc"))

    def get_synapse_state(self):
        """
        Provides Synapse's state.
        @return: Synapse's state (possible values: Up, Down)
        @rtype: String
        """
        return self._get_field("synapseState")

    def get_properties(self):
        return self._get_list_field("properties", PropertyFactory())

    def show(self, as_json = False, indent = 0):
        """
        Prints instance's information to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        if as_json:
            self.print_json()
        else:
            print " "*indent, "State:", self.get_state()
            print " "*indent, "Synapse state:", self.get_synapse_state()
            print " "*indent, "IP:", self.get_ip()
            print " "*indent, "Hostname:", self.get_hostname()
            print " "*indent, "Vnc:"
            self.get_vnc().show(indent + 2)

    def show_properties(self, indent = 0):
        print " "*indent, "Properties:"
        props = self.get_properties()
        for p in props:
            if not p.get_key() in ("ip", "hostname", "synapseState"):
                print " "*(indent + 2), p.get_key(), ":", p.get_value()


class Task(JsonWrapper):
    def __init__(self, json_data = None):
        super(Task, self).__init__(json_data)

    def get_description(self):
        return self._get_field("description")

    def get_status(self):
        return self._get_field("status")

    def show(self, indent = 0):
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Status:", self.get_status()

class TaskFactory(object):
    def new_object(self, json_data):
        return Task(json_data)


class Change(JsonWrapper):
    def __init__(self, json_data = None):
        super(Change, self).__init__(json_data)

    def get_description(self):
        return self._get_field("description")

    def get_tasks(self):
        return self._get_list_field("tasks", TaskFactory())

    def show(self, indent = 0):
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Tasks:"
        tasks = self.get_tasks()
        for t in tasks:
            t.show(indent + 2)


class Host(Resource):
    """
    A host. A host is part of an environment and has settings and properties
    associated to it. It features a list of installed applications, is associated
    to a platform and a distribution. It may be started, paused, resumed, shutdown
    and provisioned.
    """
    def __init__(self, collection, json_data = None):
        """
        @param api: An access point.
        @type api: L{CortexApi}
        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict, list or String
        """
        super(Host, self).__init__(collection, json_data)

    def get_uuid(self):
        return self._get_field("uuid")

    def get_organization(self):
        """
        Provides the organization this host is part of. It is this host's
        environment's organization.
        @return: Organization's UUID
        @rtype: String
        """
        return self._get_field("organization")

    def set_organization(self, name):
        return self._set_field("organization", name)

    def get_environment(self):
        """
        Provides the environment this host is part of.
        @return: Environment's UUID
        @rtype: String
        """
        return self._get_field("environment")

    def set_environment(self, name):
        return self._set_field("environment", name)

    def get_platform(self):
        """
        Provides the environment this host is part of.
        @return: Environment's UUID
        @rtype: String
        """
        return self._get_field("platform")

    def set_platform(self, platform):
        """
        Sets host's platform.
        @param platform: Platform's UUID
        @type platform: String
        """
        self._set_field("platform", platform)

    def set_platform_context(self, context):
        try:
            self._get_client().create(self._get_path() + "platform/", context)
        except ApiException, e:
            raise PythonApiException("Could not set distribution context: " + e.message)

    def get_distribution(self):
        """
        Provides the environment this host is part of.
        @return: Environment's UUID
        @rtype: String
        """
        return self._get_field("distribution")

    def set_distribution(self, distribution):
        """
        Sets host's distribution.
        @param distribution: Distribution's UUID
        @type distribution: String
        """
        self._set_field("distribution", distribution)

    def set_distribution_context(self, context):
        try:
            self._get_client().create(self._get_path() + "distribution/", context)
        except ApiException, e:
            raise PythonApiException("Could not set distribution context: " + e.message)

    def get_settings(self):
        """
        Provides host's settings.
        @return: Host's settings.
        @rtype: list of L{Setting}
        """
        return self._get_list_field("settings", SettingFactory(self.settings()))

    def set_settings(self, settings):
        """
        Sets host's settings. Note that, for a provisioned host, settings must
        be added, removed and/or updated using change requests.
        @return: Host's settings.
        @rtype: list of L{Setting}
        """
        self._set_list_field("settings", settings)

    def add_setting(self, setting):
        """
        Adds a setting to host. Note that, for a provisioned host, settings must
        be added, removed and/or updated using change requests.
        @param setting: A setting.
        @type setting: {Setting}
        """
        self._add_to_list_field("settings", setting)

    def get_applications(self):
        """
        Provides host's applications.
        @return: Application names
        @rtype: list of L{String}
        """
        return self._get_list_field("applications", StringFactory())

    def set_applications(self, applications):
        """
        Sets host's applications. Note that, for a provisioned host, applications
        must be added or removed using change requests.
        @param applications: Host's applications.
        @type applications: list of L{String}
        """
        self._set_list_field("applications", applications)

    def add_application(self, app_name):
        """
        Adds an application to this host. Note that, for a provisioned host,
        applications must be added or removed using change requests.
        @param application: An application's name
        @type application: L{String}
        """
        self._add_to_list_field("applications", app_name)

    def get_version(self):
        """
        Provides the version number of this host.
        @return: Host's version number
        @rtype: Integer
        """
        return int(self._get_field("version"))

    def delete(self):
        """
        Deletes this host.
        """
        try:
            self._get_client().delete(self._get_path())
        except ApiException, e:
            raise PythonApiException("Unable to delete host: " + e.message)

    def deleteInstance(self):
        try:
            self._get_client().delete(self._get_path() + "instance")
        except ApiException, e:
            raise PythonApiException("Unable to delete instance: " + e.message)

    def get_state(self):
        """
        Provides host's state.
        @return: Host's state
        @rtype: String
        """
        return self._get_field("state")

    def get_instance(self):
        """
        Provides host's instance information.
        @return: Host's instance information.
        @rtype: L{InstanceInfo}
        @raise PythonApiException: If host was not yet provisioned
        """
        if self.get_state() == "DEFINED":
            raise PythonApiException("Host must first be provision(ed|ing)")

        info_json = self._get_client().read(self._get_path() + "instance")
        return Instance(info_json)

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Organization:", self.get_organization()
        print " "*indent, "Environment:", self.get_environment()
        print " "*indent, "Platform:", self.get_platform()
        print " "*indent, "Distribution:", self.get_distribution()
        print " "*indent, "State:", self.get_state()

    def show_settings(self, indent = 0):
        """
        Prints Host's settings to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        print " "*indent, "Settings:"
        settings = self.get_settings()
        for s in settings:
            s.show(indent = (indent + 2))
            print

    def show_applications(self, indent = 0):
        print " "*indent, "Applications:"
        apps = self.get_applications()
        for app in apps:
            print " "*(indent + 2), app

    def set_instance_properties(self, props):
        client = self._get_client()
        try:
            client.create(self._get_path() + "instance/properties", props, decode = False)
        except ApiException, e:
            raise PythonApiException("Unable to set instance properties: " + e.message)

    def provision(self):
        """
        Provisions host.
        @raise PythonApiException: If host could not be provisioned.
        """
        client = self._get_client()
        try:
            client.create(self._get_path() + "instance", decode = False)
        except ApiException, e:
            raise PythonApiException("Unable to provision host: " + e.message)

    def start(self):
        """
        Starts host.
        @raise PythonApiException: If host could not be started.
        """
        try:
            result = self._get_client().update(self._get_path() + "instance/_start", decode = False)
            if(result.getcode() != 202):
                raise PythonApiException("Call not accepted by server")
        except ApiException, e:
            raise PythonApiException("Unable to start host: " + e.message)

    def pause(self):
        """
        Pauses host.
        @raise PythonApiException: If host could not be paused.
        """
        result = self._get_client().update(self._get_path() + "instance/_pause", decode = False)
        if(result.getcode() != 202):
            raise PythonApiException("Call not accepted by server")

    def resume(self):
        """
        Resumes host's execution (after pause).
        @raise PythonApiException: If host's execution could not be resumed.
        """
        result = self._get_client().update(self._get_path() + "instance/_resume", decode = False)
        if(result.getcode() != 202):
            raise PythonApiException("Call not accepted by server")

    def shutdown(self):
        """
        Shutdowns host.
        @raise PythonApiException: If host could not be shutdown.
        """
        result = self._get_client().update(self._get_path() + "instance/_stop", decode = False)
        if(result.getcode() != 202):
            raise PythonApiException("Call not accepted by server")

    def poweroff(self):
        """
        Power-off host.
        @raise PythonApiException: If host could not be powered-off.
        """
        try:
            result = self._get_client().update(self._get_path() + "instance/_off", decode = False)
            if(result.getcode() != 202):
                raise PythonApiException("Call not accepted by server")
        except ApiException, e:
            raise PythonApiException("Unable to poweroff host: " + e.message)

    def render_file(self, app_name, file_name):
        try:
            result = self._get_client().read(self._get_path() + "applications/" + app_name + "/files/" + file_name, decode = False)
            return result
        except ApiException, e:
            raise PythonApiException("Unable to render file: " + e.message)

    def render_kickstart(self):
        try:
            result = self._get_client().read(self._get_path() + "kickstart", decode = False)
            return result
        except ApiException, e:
            raise PythonApiException("Unable to render kickstart: " + e.message)

    def clone(self):
        try:
            result = self._get_client().update(self._get_path() + "_clone")
            return Host(result)
        except ApiException, e:
            raise PythonApiException("Unable to clone host: " + e.message)

    def install_application(self, context):
        if self.get_state() != "PROVISIONED":
            raise PythonApiException("Host must be provisioned")

        if context.get_application() in self.get_applications():
            raise PythonApiException("Application is already installed")

        try:
            self._get_client().create(self._get_path() + "applications/", context.get_json())
        except ApiException, e:
            raise PythonApiException("Unable to install application: " + e.message)

    def uninstall_application(self, app_name):
        if self.get_state() != "PROVISIONED":
            raise PythonApiException("Host must be provisioned")

        if not app_name in self.get_applications():
            raise PythonApiException("Application is not installed")

        try:
            self._get_client().delete(self._get_path() + "applications/" + app_name)
        except ApiException, e:
            raise PythonApiException("Unable to uninstall application: " + e.message)

    def settings(self):
        return SettingCollection(self._get_api(), self._get_path() + "settings/")

    def application_settings(self, app_name):
        return SettingCollection(self._get_api(), self._get_path() + "applications/" + app_name + "/settings/")

    def platform_settings(self):
        return SettingCollection(self._get_api(), self._get_path() + "platform/settings/")

    def distribution_settings(self):
        return SettingCollection(self._get_api(), self._get_path() + "distribution/settings/")

    def get_changes(self):
        if self.get_state() != "PROVISIONED":
            raise PythonApiException("Host must be provisioned")

        try:
            json_changes = self._get_client().read(self._get_path() + "changes/")
            changes = []
            if json_changes["count"] == "0":
                return changes

            for json_change in json_changes["items"]:
                changes.append(Change(json_change))
            return changes
        except ApiException, e:
            raise PythonApiException("Unable to get changes: " + e.message)
