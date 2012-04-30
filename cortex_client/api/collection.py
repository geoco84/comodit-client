# coding: utf-8
"""
Base collection class module. Cortex server maintains collections of resources.
Resources are listed, retrieved and created through these collections. This
module defines the base resource collection.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from cortex_client.api.exceptions import PythonApiException
from cortex_client.rest.exceptions import ApiException

class ResourceNotFoundException(PythonApiException):
    """
    Exception raised when a resource was not found in a collection.
    """
    def __init__(self, identifier):
        """
        Creates an instance of ResourceNotFoundException.

        @param identifier: The identifier of the resource.
        @type identifier: String
        """
        super(ResourceNotFoundException, self).__init__("Resource not found: " + identifier)

class Collection(object):
    """
    Base resources collection. Cortex server maintains collections of resources.
    Resources are listed, retrieved and created through these collections.
    Most common operations are already implemented by this class. Subclasses
    must at least implement L{_new_resource} and L{get_uuid} methods.
    """

    def __init__(self, resource_path, api):
        """
        Creates an instance of Collection.

        @param resource_path: Path to associated collection on cortex server
        (for example, 'organizations' is the relative path to access organizations
        collection i.e., if server's API is available at address
        'http://cortex.server.com/api', applications collection is available
        at address 'http://cortex.server.com/api/organizations'.
        @type resource_path: String
        @param api: An API access point.
        @type api: L{CortexApi}
        """
        self._resource_path = resource_path
        self._api = api

    def get_api(self):
        return self._api

    def get_client(self):
        return self._api.get_client()

    def get_path(self):
        """
        Returns the relative path to associated collection.

        @return: A relative path
        @rtype: String

        @see: L{__init__}
        """
        return self._resource_path

    def add_resource(self, resource, parameters = {}):
        """
        Adds a resource to this collection. A call to this method actually
        creates a new resource on the server. State of the object may be
        updated (in particular, UUID is available as it is associated by
        server).
        
        @param resource: A resource to add to the collection.
        @type resource: L{Resource}
        
        @raise PythonApiException: If the resource could not be created on the
        server.
        """
        try:
            result = self._api.get_client().create(self._resource_path,
                                                   resource.get_json(),
                                                   parameters = parameters)
        except ApiException, e:
            raise PythonApiException("Could not create resource: " + e.message)
        resource.set_json(result)

    def get_resources(self):
        """
        Provides the list of resources associated to this collection.
        
        @return: A list of resources
        @rtype: list of L{Resource}
        """
        client = self._api.get_client()
        try:
            result = client.read(self._resource_path)

            resources_list = []
            count = int(result["count"])
            if(count > 0):
                json_list = result["items"]
                for json_res in json_list:
                    resources_list.append(self._new_resource(json_res))

            return resources_list
        except ApiException, e:
            if e.code == 404:
                raise ResourceNotFoundException(e.message)
            else:
                raise PythonApiException("Could not get elements: " + e.message)

    def _new_resource(self, json_data = None):
        """
        Instantiates a new resource object. New object's state is set using
        provided JSON data (organized as a dict).

        @param json_data: Initial state of object to instantiate
        @type json_data: C{dict}

        @return: A resource object
        @rtype: L{Resource}
        """
        raise NotImplementedError

    def get_resource(self, e_id):
        """
        Retrieves the resource or collection with given identifier from this collection.
        
        @param e_id: The identifier of the resource or collection to retrieve
        @type e_id: String
        
        @return: A resource
        @rtype: L{Resource}
        
        @raise PythonApiException: If the resource could not be retrieved from
        server.
        """
        client = self._api.get_client()
        try:
            result = client.read(self._resource_path + e_id)
            return self._new_resource(result)
        except ApiException, e:
            if e.code == 404:
                raise ResourceNotFoundException(e_id)
            else:
                raise PythonApiException("Could not get resource " + e_id + ":" + e.message)

    def get_single_resource(self):
        return self.get_resource("")

    def clear_collection(self, parameters = {}):
#        try:
            self._api.get_client().delete(self._resource_path,
                                          parameters = parameters)
#        except ApiException, e:
#            raise PythonApiException("Could not delete resource: " + e.message)
