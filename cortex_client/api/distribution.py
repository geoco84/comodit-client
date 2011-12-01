# coding: utf-8
"""
Distribution module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from resource import Resource
from file import File

class Distribution(Resource):
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

    def _get_kickstart_path(self):
        return self._get_path() + "kickstart"

    def get_kickstart(self):
        """
        Provides the UUID of kickstart's template.
        @return: Kickstart's template (UUID)
        @rtype: L{File}
        """
        data = self._get_field("kickstart")
        if data is None:
            return None
        return File(json_data = data)

    def set_kickstart(self, kickstart):
        """
        Sets the UUID of kickstart's template.
        @param kickstart: Kickstart's template
        @type kickstart: L{File}
        """
        self._set_field("kickstart", kickstart.get_json())

    def set_kickstart_content(self, path):
        self._get_client().upload_to_exising_file_with_path(path, self._get_kickstart_path())

    def get_kickstart_content(self):
        return self._get_client().read(self._get_kickstart_path(), decode = False)

    def get_initrd(self):
        """
        Provides the path to distribution's initrd.
        @return: A path
        @rtype: String
        """
        return self._get_field("initrd")

    def set_initrd(self, initrd):
        """
        Sets the path to distribution's initrd.
        @param initrd: A path
        @type initrd: String
        """
        return self._set_field("initrd", initrd)

    def get_vmlinuz(self):
        """
        Provides the path to distribution's vmlinuz.
        @return: A path
        @rtype: String
        """
        return self._get_field("vmlinuz")

    def set_vmlinuz(self, vmlinuz):
        """
        Sets the path to distribution's vmlinuz.
        @param vmlinuz: A path
        @type vmlinuz: String
        """
        return self._set_field("vmlinuz", vmlinuz)

    def get_version(self):
        """
        Provides distribution's version.
        @return: Distribution's version
        @rtype: Integer
        """
        return int(self._get_field("version"))

    def _show(self, indent = 0):
        super(Distribution, self)._show(indent)
        kickstart = self.get_kickstart()
        if kickstart:
            print " "*indent, "Kickstart:"
            kickstart.show(indent = indent + 2)
        print " "*indent, "Initrd:", self.get_initrd()
        print " "*indent, "Vmlinuz:", self.get_vmlinuz()
