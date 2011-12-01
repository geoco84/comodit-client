# coding: utf-8
"""
Cortex server access point module. An instance of CortexApi class provides an
access to resources and services exhibited by a particular cortex-server.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from cortex_client.rest.client import Client
from rendering_service import RenderingService
from organization_collection import OrganizationCollection
from user_collection import UserCollection

from organization import Organization
from user import User

class CortexApi(object):
    """
    Defines the access point to a particular cortex server. An instance of
    CortexApi class may be used to retrieve, create, update and delete resources
    of the server (hosts, applications, etc.).

    Resources handled by the server may listed and accessed using collections.
    There is one collection by resource type (for example, all applications
    defined on a server are part of application collection).
    A collection getter is a method that provides an access point to a collection
    of resources. This class provides all collection getters. These methods
    are named as follows: get_*_collection where * is a resource type.

    Factory methods defined by this class allow to instantiate access points to
    resources (application, distribution, host, etc.) managed by a cortex server.
    These factory methods are named as follows: new_* where * is a resource type.

    Finally, this class defines getters that provide services implemented by the
    server or this client. Currently, 2 services are defined: the directory and
    the rendering service. The directory allows to retrieve the UUID of a
    resource given an identifier (a name or a path). The rendering service
    provides the result of templates' rendering for a particular host.
    """

    def __init__(self, endpoint, username, password):
        """
        Creates an instance of CortexApi using given parameters to connect to
        the server. These parameters include the URL of cortex server's API and
        a user name and a password for authentication.
        
        @param endpoint: The URL of a cortex-server's REST API.
        @type endpoint: String
        @param username: A user name
        @type username: String
        @param password: A password
        @type password: String
        """

        self._client = Client(endpoint, username, password)
        self._rendering = RenderingService(self)

        self._orga_collection = OrganizationCollection(self)
        self._user_collection = UserCollection(self)

    def get_client(self):
        """
        Provides the REST client used by this instance to communicate with
        cortex server's API.

        @return: The REST client
        @rtype: L{Client}
        """
        return self._client

    def get_rendering_service(self):
        """
        Provides the rendering service associated to this instance.

        @return: A rendering service instance.
        @rtype: L{RenderingService}
        """
        return self._rendering

    def organizations(self):
        """
        Provides an access to organizations collection of associated cortex server.
        
        @return: The organizations collection access point
        @rtype: L{OrganizationCollection}
        """
        return self._orga_collection

    def users(self):
        """
        Provides an access to users collection of associated cortex server.
        
        @return: The users collection access point
        @rtype: L{UserCollection}
        """
        return self._user_collection

    def new_organization(self, name):
        """
        Factory method for organization resource.

        @return: An organization connected to associated cortex server.
        @rtype: L{Organization}
        """
        org = Organization(self._orga_collection)
        org.set_name(name)
        return org

    def new_user(self, username):
        """
        Factory method for user resource.

        @return: A user connected to associated cortex server.
        @rtype: L{User}
        """
        user = User(self._user_collection)
        user.set_name(username)
        return user
