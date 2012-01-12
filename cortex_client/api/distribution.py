# coding: utf-8
"""
Distribution module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from file import File
from cortex_client.api.settings import SettingFactory, Configurable
from cortex_client.api.parameters import ParameterFactory

class Distribution(Configurable):
    """
    Represents a distribution. A distribution is described by a kickstart file,
    the base URL of its repository, an initrd and a vmlinuz.
    """
    def __init__(self, collection, json_data = None):
        """
        @param api: An access point.
        @type api: L{CortexApi}
        @param json_data: A quasi-JSON representation of change request's state.
        @type json_data: dict, list or String
        """
        super(Distribution, self).__init__(collection, json_data)

    def get_uuid(self):
        return self._get_field("uuid")

    def _get_file_path(self, name):
        return self._get_path() + "files/" + name + "/content"

    def get_files(self):
        data = self._get_field("files")
        if data is None:
            return None
        files = []
        for json_f in data:
            files.append(File(json_data = json_f))
        return files

    def get_file(self, name):
        files = self._get_field("files")
        if files is None:
            return None
        for json_f in files:
            f = File(json_f)
            if f.get_name() == name:
                return f
        return None

    def add_file(self, f):
        self._add_to_list_field("files", f)

    def set_file_content(self, name, path):
        self._get_client().upload_to_exising_file_with_path(path, self._get_file_path(name))

    def get_file_content(self, name):
        return self._get_client().read(self._get_file_path(name), decode = False)

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

    def get_version(self):
        """
        Provides distribution's version.
        @return: Distribution's version
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

    def _show(self, indent = 0):
        super(Distribution, self)._show(indent)
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
            f.show(indent + 2)

