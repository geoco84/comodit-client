# coding: utf-8
"""
File module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from cortex_client.util.json_wrapper import JsonWrapper
from cortex_client.api.collection import Collection
from cortex_client.api.resource import Resource


class Delimiter(JsonWrapper):
    def __init__(self, json_data = None):
        super(Delimiter, self).__init__(json_data)

    def get_start(self):
        return self._get_field("start")

    def get_end(self):
        return self._get_field("end")

    def show(self, indent = 0):
        print " "*indent, "Start:", self.get_start()
        print " "*indent, "End:", self.get_end()


class FileResource(Resource):
    def _get_content_path(self):
        return self._get_path() + "content"

    def set_content(self, path):
        self._get_client().upload_to_exising_file_with_path(path, self._get_content_path())

    def get_content(self):
        return self._get_client().read(self._get_content_path(), decode = False)


class File(FileResource):
    """
    A file template. A template is the representation of a parametrized file.
    A template may be rendered after values are given to its parameters (see
    L{RenderingService}).
    """
    def __init__(self, collection, json_data = None):
        """
        @param api: An access point.
        @type api: L{CortexApi}
        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict, list or String
        """
        super(File, self).__init__(collection, json_data)

    def get_name(self):
        """
        Provides the name of this resource or None if it is not yet set.
        
        @return: The name of this resource.
        @rtype: String
        """
        return self._get_field("name")

    def set_name(self, name):
        """
        Sets the name of this resource.

        @param name: The new name
        @type name: String
        """
        self._set_field("name", name)

    def get_delimiter(self):
        return Delimiter(self._get_field("delimiter"))

    def set_delimiter(self, delim):
        self._set_field("delimiter", delim)

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Delimiter:"
        self.get_delimiter().show(indent + 2)


class FileCollection(Collection):
    def __init__(self, api, collection_path):
        super(FileCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        res = File(self, json_data)
        return res


class FileFactory(object):
    def __init__(self, collection = None):
        self._collection = collection

    """
    Application's file factory.
    
    @see: L{Application}
    @see: L{cortex_client.util.json_wrapper.JsonWrapper._get_list_field}
    """
    def new_object(self, json_data):
        """
        Instantiates an ApplicationFile object using given state.
        
        @param json_data: A quasi-JSON representation of an ApplicationFile
        instance's state.
        @type json_data: String, dict or list
        
        @return: A file object
        @rtype: L{ApplicationFile}
        """
        return File(self._collection, json_data)
