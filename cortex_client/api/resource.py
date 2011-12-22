# coding: utf-8
"""
Base resource class module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

import os

from cortex_client.util.json_wrapper import JsonWrapper

import cortex_client.util.path as path

class Resource(JsonWrapper):
    """
    Represents a resource managed by a cortex server. An instance of this class
    may be seen as a proxy to a resource managed by a cortex-server. Note that
    alterations of a Resource instance's state are not automatically committed
    to the server. A call to L{commit} actually updates the state of the object
    on the server. In addition, this class may be instantiated in order to
    create a new resource on the server. In this case, the resource does not yet
    exist on the server and, once the state of the local object is complete,
    must be explicitly created by a call to L{create}.
    """

    def __init__(self, collection, json_data = None):
        """
        Sets the collection this resource is associated to.

        @param collection: A collection
        @type collection: L{Collection}
        """
        super(Resource, self).__init__(json_data)
        self._collection = collection

    def set_collection(self, collection):
        if collection is None:
            raise Exception("Collection must be set")
        self._collection = collection

    def get_collection(self):
        return self._collection

    def _get_path(self):
        """
        Provides the path to this resource.
        
        @return: The path to this resource
        @rtype: String
        """
        return self._collection.get_path() + self.get_name() + "/"

    def __enforce_connected(self):
        if self._collection is None:
            raise Exception("Resource is not connected")

    def _get_client(self):
        """
        Provides rest client to server.
        
        @return: The rest client
        @rtype: L{Client}
        """
        self.__enforce_connected()
        return self._collection.get_client()

    def _get_api(self):
        """
        Provides rest client to server.
        
        @return: The rest client
        @rtype: L{CortexApi}
        """
        self.__enforce_connected()
        return self._collection.get_api()

    def get_name(self):
        """
        Provides the name of this resource or None if it is not yet set.
        
        @return: The name of this resource.
        @rtype: String
        """
        return self._get_field("name")

    def get_identifier(self):
        return self.get_name()

    def set_name(self, name):
        """
        Sets the name of this resource.

        @param name: The new name
        @type name: String
        """
        self._set_field("name", name)

    def get_description(self):
        """
        Provides the description for this resource or None if it is not yet set.

        @return: The description of this resource.
        @rtype: String
        """
        return self._get_field("description")

    def set_description(self, description):
        """
        Sets the description of this resource.

        @param description: The new description
        @type description: String
        """
        self._set_field("description", description)

    def update(self):
        """
        Replaces the state of this object with state retrieved from server.

        @raise PythonApiException: If server access point is not set.
        """
        self.set_json(self._get_client().read(self._get_path()))

    def rename(self, new_name):
        current_path = self._get_path()
        self.set_name(new_name)
        self.set_json(self._get_client().update(current_path, self.get_json()))

    def commit(self, force = False):
        """
        Updates the state of the resource on the server with state of local
        object.

        @param force: Update is forced
        @type force: Boolean

        @raise PythonApiException: If server access point is not set.
        """
        parameters = {}
        if(force):
            parameters["force"] = "true"
        self.set_json(self._get_client().update(self._get_path(),
                                        self.get_json(),
                                        parameters))

    def create(self):
        """
        Creates a new resource on the server using this object's state for
        initialization.

        @raise PythonApiException: If server access point is not set.
        """
        self.__enforce_connected()
        self._collection.add_resource(self)

    def delete(self):
        """
        Deletes associated resource on the server.

        @raise PythonApiException: If server access point is not set.
        """
        self.__enforce_connected()
        self._get_client().delete(self._get_path())

    def show(self, as_json = False, indent = 0):
        """
        Prints this resource's state to standard output. The state may be
        indented. It can also be displayed using JSON format.

        @param as_json: If True, resource's state is displayed in JSON format.
        Otherwise, it is displayed in a more user-friendly way.
        @type as_json: Boolean
        @param indent: The number of spaces to put in front of each displayed
        line (only if as_json is False).
        @type indent: Integer
        """
        if(as_json):
            self.print_json()
        else:
            self._show(indent)

    def _show(self, indent = 0):
        """
        Prints this resource's state to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()

    def dump(self, dest_folder):
        """
        Dumps the state of this object in given folder. Several files may be
        created in destination folder, as well as sub-folders.
        
        @param dest_folder: The path to destination folder
        @type dest_folder: String
        """
        path.ensure(dest_folder)
        plat_file = os.path.join(dest_folder, "definition.json")
        self.dump_json(plat_file)

    def load(self, input_folder):
        """
        Loads the state of this object from files contained by given folder.
        
        @param input_folder: Path to source folder
        @type input_folder: String
        """
        self.load_json(os.path.join(input_folder, "definition.json"))

