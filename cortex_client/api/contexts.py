from cortex_client.util.json_wrapper import JsonWrapper
from cortex_client.api.settings import SettingFactory


class AbstractContext(JsonWrapper):
    def __init__(self, json_data = None):
        super(AbstractContext, self).__init__(json_data)

    def get_settings(self):
        return self._get_list_field("settings", SettingFactory(None))

    def add_setting(self, setting):
        self._add_to_list_field("settings", setting)

    def get_setting(self, key):
        return self._get_field("settings").get(key)


class ApplicationContext(AbstractContext):
    def __init__(self, json_data = None):
        super(ApplicationContext, self).__init__(json_data)

    def get_application(self):
        return self._get_field("application")

    def set_application(self, application):
        return self._set_field("application", application)


class DistributionContext(AbstractContext):
    def __init__(self, json_data = None):
        super(DistributionContext, self).__init__(json_data)

    def get_distribution(self):
        return self._get_field("distribution")

    def set_distribution(self, distribution):
        return self._set_field("distribution", distribution)


class PlatformContext(AbstractContext):
    def __init__(self, json_data = None):
        super(PlatformContext, self).__init__(json_data)

    def get_platform(self):
        return self._get_field("platform")

    def set_platform(self, platform):
        return self._set_field("platform", platform)
