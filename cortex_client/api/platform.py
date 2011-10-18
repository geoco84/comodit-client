from resource import Resource
from host import SettingFactory

class Platform(Resource):
    def __init__(self, json_data = None):
        from platform_collection import PlatformCollection
        super(Platform, self).__init__(PlatformCollection(), json_data)

    def get_driver(self):
        return self._get_field("driver")

    def set_driver(self, owner):
        return self._set_field("driver", owner)

    def get_owner(self):
        return self._get_field("owner")

    def set_owner(self, owner):
        return self._set_field("owner", owner)

    def get_settings(self):
        return self._get_list_field("settings", SettingFactory())

    def set_settings(self, owner):
        return self._set_list_field("settings", owner)

    def _show(self, indent = 0):
        super(Platform, self)._show(indent)
        print " "*indent, "Driver:", self.get_driver()
        print " "*indent, "Owner:", self.get_owner()
        print " "*indent, "Settings:"
        settings = self.get_settings()
        for s in settings:
            s.show(indent + 2)
