# coding: utf-8
"""
Platform module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from host import SettingFactory
from cortex_client.api.file import File, FileFactory
from cortex_client.api.settings import Configurable
from cortex_client.api.parameters import ParameterFactory, Parameter
from cortex_client.api.collection import Collection


class PlatformFileCollection(Collection):
    def __init__(self, api, collection_path):
        super(PlatformFileCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        res = File(self, json_data)
        return res


class PlatformParameterCollection(Collection):
    def __init__(self, api, collection_path):
        super(PlatformParameterCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        res = Parameter(self, json_data)
        return res


class Platform(Configurable):
    """
    Platform's description. A platform is described by a driver and a list of
    settings.
    """
    def __init__(self, collection, json_data = None):
        """
        @param api: An access point.
        @type api: L{CortexApi}
        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict, list or String
        """
        super(Platform, self).__init__(collection, json_data)

    def get_uuid(self):
        return self._get_field("uuid")

    def get_driver(self):
        """
        Provides platform's driver class name.
        @return: Driver's class name
        @rtype: String
        """
        return self._get_field("driver")

    def set_driver(self, driver):
        """
        Sets platform's driver class name.
        @param driver: Driver's class name
        @type driver: String
        """
        return self._set_field("driver", driver)

    def get_settings(self):
        """
        Provides platform's settings.
        @return: A list of settings
        @rtype: list of L{Setting}
        """
        return self._get_list_field("settings", SettingFactory(None))

    def set_settings(self, settings):
        """
        Sets platform's settings.
        @param settings: A list of settings
        @type settings: list of L{Setting}
        """
        return self._set_list_field("settings", settings)

    def add_setting(self, setting):
        """
        Adds a setting to platform.
        @param setting: A setting
        @type setting: L{Setting}
        """
        self._add_to_list_field("settings", setting)

    def _get_file_path(self, name):
        return self._get_path() + "files/" + name + "/content"

    def files(self):
        return PlatformFileCollection(self._get_api(), self._get_path() + "files/")

    def get_files(self):
        return self._get_list_field("files", FileFactory(None))

    def get_file(self, name):
        files = self._get_field("files")
        if files is None:
            return None
        for json_f in files:
            f = File(None, json_f)
            if f.get_name() == name:
                return f
        return None

    def add_file(self, f):
        self._add_to_list_field("files", f)

    def set_file_content(self, name, path):
        self._get_client().upload_to_exising_file_with_path(path, self._get_file_path(name))

    def get_file_content(self, name):
        return self._get_client().read(self._get_file_path(name), decode = False)

    def get_version(self):
        """
        Provides platform's version number.
        @return: A version number
        @rtype: Integer
        """
        return int(self._get_field("version"))

    def get_parameters(self):
        """
        Provides the list of parameters associated to this template.
        @return: The list of parameters
        @rtype: list of L{Parameter}
        """
        return self._get_list_field("parameters", ParameterFactory())

    def add_parameter(self, parameter):
        """
        Adds a parameter to the list of parameters associated to this template.
        @param parameter: The parameter
        @type parameter: L{Parameter}
        """
        self._add_to_list_field("parameters", parameter)

    def parameters(self):
        return PlatformParameterCollection(self._get_api(), self._get_path() + "parameters/")

    def _show(self, indent = 0):
        super(Platform, self)._show(indent)
        print " "*indent, "Driver:", self.get_driver()
        print " "*indent, "Settings:"
        settings = self.get_settings()
        for s in settings:
            s._show(indent + 2)
        print " "*indent, "Parameters:"
        params = self.get_parameters()
        for p in params:
            p.show(indent + 2)
        print " "*indent, "Files:"
        files = self.get_files()
        for f in files:
            f._show(indent + 2)
