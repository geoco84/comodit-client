import os

import cortex_client.util.path as path

from resource import Resource
from host import SettingFactory

class Platform(Resource):
    def __init__(self, api, json_data = None):
        super(Platform, self).__init__(api, api.get_platform_collection(), json_data)

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

    def get_version(self):
        return self._get_field("version")

    def dump(self, dest_folder):
        path.ensure(dest_folder)
        plat_file = os.path.join(dest_folder, "definition.json")
        self.dump_json(plat_file)

    def load(self, input_folder):
        raise NotImplementedError

    def _show(self, indent = 0):
        super(Platform, self)._show(indent)
        print " "*indent, "Driver:", self.get_driver()
        print " "*indent, "Owner:", self.get_owner()
        print " "*indent, "Settings:"
        settings = self.get_settings()
        for s in settings:
            s.show(indent + 2)
