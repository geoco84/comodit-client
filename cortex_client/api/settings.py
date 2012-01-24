# coding: utf-8

from cortex_client.api.resource import Resource
from cortex_client.api.collection import Collection

class Setting(Resource):
    """
    A host's setting. A setting has a key, a value and a version number. Note
    that in order to add a setting to a host, a change request must be used. Same
    applies to setting's deletion and update. Therefore, a setting does not
    feature setters.
    """
    def __init__(self, collection, json_data = None):
        super(Setting, self).__init__(collection, json_data)

    def get_identifier(self):
        return self.get_key()

    def get_name(self):
        return self.get_key()

    def set_name(self, name):
        self.set_key(name)

    def get_value(self):
        return self._get_field("value")

    def set_value(self, value):
        self._set_field("value", value)
        self._del_field("link")
        self._del_field("property")

    def get_link(self):
        return self._get_field("link")

    def set_link(self, value):
        self._del_field("value")
        self._set_field("link", value)
        self._del_field("property")

    def get_property(self):
        return self._get_field("property")

    def set_property(self, value):
        self._del_field("value")
        self._del_field("link")
        self._set_field("property", value)

    def set_key(self, key):
        self._set_field("key", key)

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

    def _show(self, indent = 0):
        """
        Prints this property's state to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        print " "*indent, "Key:", self.get_key()
        if self.get_value() != None:
            print " "*indent, "Value:", self.get_value()
        elif self.get_value() != None:
            print " "*indent, "Link:", self.get_link()
        elif self.get_value() != None:
            print " "*indent, "Porperty:", self.get_property()


class SettingFactory(object):

    def __init__(self, collection):
        self._collection = collection

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
        return Setting(self._collection, json_data)


class SettingCollection(Collection):
    def __init__(self, api, collection_path):
        super(SettingCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        return Setting(self, json_data)

class Configurable(Resource):
    def settings(self):
        return SettingCollection(self._get_api(), self._get_path() + "settings/")

    def new_setting(self, key):
        setting = Setting(self.settings())
        setting.set_key(key)
        return setting

    def _show_settings(self, indent = 0):
        settings = self.settings().get_resources()
        print " "*indent, "Settings:"
        for s in settings:
            s._show(indent + 2)
