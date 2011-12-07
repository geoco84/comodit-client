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

class Setting(JsonWrapper):
    """
    A host's setting. A setting has a key, a value and a version number. Note
    that in order to add a setting to a host, a change request must be used. Same
    applies to setting's deletion and update. Therefore, a setting does not
    feature setters.
    """
    def __init__(self, json_data = None):
        super(Setting, self).__init__(json_data)

    def get_value(self):
        """
        Provides setting's value.
        @return: The value
        @rtype: String
        """
        return self._get_field("value")

    def get_key(self):
        """
        Provides setting's key.
        @return: The key
        @rtype: String
        """
        return self._get_field("key")

    def get_version(self):
        """
        Provides setting's version number.
        @return: The version number
        @rtype: Integer
        """
        return int(self._get_field("version"))

    def show(self, indent = 0):
        """
        Prints this property's state to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        print " "*indent, "Key:", self.get_key()
        print " "*indent, "Value:", self.get_value()
        print " "*indent, "Version:", self.get_version()


class SettingFactory(object):
    """
    Host's setting factory.
    
    @see: L{Setting}
    @see: L{cortex_client.util.json_wrapper.JsonWrapper._get_list_field}
    """
    def new_object(self, json_data):
        """
        Instantiates a L{Setting} object using given state.
        
        @param json_data: A quasi-JSON representation of a Property instance's state.
        @type json_data: String, dict or list
        
        @return: A setting
        @rtype: L{Setting}
        """
        return Setting(json_data)


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

    def show(self, indent = 0):
        """
        Prints instance's information to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
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

    def get_settings(self):
        """
        Provides host's settings.
        @return: Host's settings.
        @rtype: list of L{Setting}
        """
        return self._get_list_field("settings", SettingFactory())

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

    def get_properties(self):
        """
        Provides host's properties.
        @return: Host's properties.
        @rtype: list of L{Property}
        """
        return self._get_list_field("properties", PropertyFactory())

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

    def delete(self, delete_vm = False):
        """
        Deletes this host. Associated VM may also be destroyed.
        @param delete_vm: If True, VM associated to this host is destroyed.
        """
        if(delete_vm):
            try:
                self._get_client().update(self._get_path() + "instance/_delete",
                                              decode = False)
            except ApiException, e:
                if(e.code == 400):
                    print "Could not delete VM:", e.message
                else:
                    raise e
        self._get_client().delete(self._get_path())

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

    def provision(self):
        """
        Provisions host.
        @raise PythonApiException: If host could not be provisioned.
        """
        client = self._get_client()
        try:
            client.update(self._get_path() + "_provision", decode = False)
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
