import os

import cortex_client.util.path as path

from resource import Resource
from cortex_client.api.file_collection import FileCollection

class Distribution(Resource):
    def __init__(self, json_data = None):
        from distribution_collection import DistributionCollection
        super(Distribution, self).__init__(DistributionCollection(), json_data)

    def get_kickstart(self):
        return self._get_field("kickstart")

    def set_kickstart(self, kickstart):
        return self._set_field("kickstart", kickstart)

    def get_url(self):
        return self._get_field("url")

    def set_url(self, url):
        return self._set_field("url", url)

    def get_initrd(self):
        return self._get_field("initrd")

    def set_initrd(self, initrd):
        return self._set_field("initrd", initrd)

    def get_vmlinuz(self):
        return self._get_field("vmlinuz")

    def set_vmlinuz(self, vmlinuz):
        return self._set_field("vmlinuz", vmlinuz)

    def get_owner(self):
        return self._get_field("owner")

    def set_owner(self, owner):
        return self._set_field("owner", owner)

    def get_version(self):
        return self._get_field("version")

    def dump(self, output_folder):
        dist_folder = os.path.join(output_folder, self.get_name())
        path.ensure(dist_folder)
        self.dump_json(os.path.join(dist_folder, "definition.json"))

        # Dump kickstart
        kickstart = FileCollection().get_resource(self.get_kickstart())
        kickstart.dump(dist_folder, "kickstart")

    def _show(self, indent = 0):
        super(Distribution, self)._show(indent)
        print " "*indent, "Kickstart:", self.get_kickstart()
        print " "*indent, "URL:", self.get_url()
        print " "*indent, "Initrd:", self.get_initrd()
        print " "*indent, "Vmlinuz:", self.get_vmlinuz()
        print " "*indent, "Owner:", self.get_owner()
