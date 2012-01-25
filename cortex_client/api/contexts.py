from cortex_client.api.settings import SettingFactory, Configurable, Setting
from cortex_client.api.exceptions import PythonApiException
from cortex_client.api.collection import Collection

class AbstractContext(Configurable):
    def __init__(self, collection, json_data = None):
        super(AbstractContext, self).__init__(collection, json_data)

    def get_settings(self):
        return self._get_list_field("settings", SettingFactory(self.settings()))

    def add_simple_setting(self, key, value):
        setting = Setting(self.settings())
        setting.set_key(key)
        setting.set_value(value)
        self._add_to_list_field("settings", setting)

    def add_link_setting(self, key, link, default):
        setting = Setting(self.settings())
        setting.set_key(key)
        setting.set_link(link, default)
        self._add_to_list_field("settings", setting)

    def add_property_setting(self, key, prop):
        setting = Setting(self.settings())
        setting.set_key(key)
        setting.set_property(prop)
        self._add_to_list_field("settings", setting)

    def get_setting(self, key):
        return Setting(self.settings(), self._get_field("settings").get(key))

    def rename(self, new_name):
        raise PythonApiException("Renaming is unsupported for contexts")

    def commit(self, force = False):
        raise PythonApiException("Committing is unsupported for contexts")


class ApplicationContextCollection(Collection):
    def __init__(self, api, collection_path):
        super(ApplicationContextCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data = None):
        return ApplicationContext(self, json_data)


class ApplicationContext(AbstractContext):
    def __init__(self, collection, json_data = None):
        super(ApplicationContext, self).__init__(collection, json_data)

    def _get_path(self):
        return self._collection.get_path() + self.get_application() + "/"

    def get_identifier(self):
        return self.get_application()

    def get_name(self):
        return self.get_application()

    def get_application(self):
        return self._get_field("application")

    def set_application(self, application):
        return self._set_field("application", application)

    def _show(self, indent = 0):
        print " "*indent, "Application:", self.get_application()
        self._show_settings(indent)


class DistributionContextCollection(Collection):
    def __init__(self, api, collection_path):
        super(DistributionContextCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        return DistributionContext(self, json_data)


class DistributionContext(AbstractContext):
    def __init__(self, collection, json_data = None):
        super(DistributionContext, self).__init__(collection, json_data)

    def _get_path(self):
        return self._collection.get_path()

    def get_distribution(self):
        return self._get_field("distribution")

    def set_distribution(self, distribution):
        return self._set_field("distribution", distribution)

    def _show(self, indent = 0):
        print " "*indent, "Distribution:", self.get_distribution()
        self._show_settings(indent)


class PlatformContextCollection(Collection):
    def __init__(self, api, collection_path):
        super(PlatformContextCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        return PlatformContext(self, json_data)


class PlatformContext(AbstractContext):
    def __init__(self, collection, json_data = None):
        super(PlatformContext, self).__init__(collection, json_data)

    def _get_path(self):
        return self._collection.get_path()

    def get_platform(self):
        return self._get_field("platform")

    def set_platform(self, platform):
        return self._set_field("platform", platform)

    def _show(self, indent = 0):
        print " "*indent, "Platform:", self.get_platform()
        self._show_settings(indent)
