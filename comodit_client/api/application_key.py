# coding: utf-8
"""
Provides the classes related to application key entity: L{ApplicationKey}
and L{ApplicationKeyCollection}.
"""

from collection import Collection
from comodit_client.api.entity import Entity


class ApplicationKeyCollection(Collection):
    """
    Collection of application keys. An application key collection is owned by an
    L{Organization}.
    """

    def _new(self, json_data = None):
        return ApplicationKey(self, json_data)

    def new(self, token):
        """
        Instantiates a new application key object.

        @param name: The name of new application key.
        @type name: string
        @rtype: L{ApplicationKey}
        """

        key = self._new()
        key.token = token
        return key

    def create(self, token):
        """
        Creates a remote application key entity and returns associated local
        object.

        @param name: The name of new application key.
        @type name: string
        @rtype: L{ApplicationKey}
        """

        key = self.new(token)
        key.create()
        return key


class ApplicationKey(Entity):
    """
    Application Key entity representation. An application key defines a token that can be used to authenticate
    and perform some action in a particular organization.
    """

    @property
    def organization(self):
        """
        The name of the organization owning this environment.

        @rtype: string
        """

        return self._get_field("organization")

    @property
    def token(self):
        """
        The token associated with this application key.

        @rtype: string
        """

        return self._get_field("token")

    @property
    def expiration_date(self):
        """
        The expiration date associated with this application key.

        @rtype: string
        """

        return self._get_field("expirationDate")
    
    @property
    def group(self):
        """
        The group associated with this application key.

        @rtype: string
        """

        return self._get_field("group")
    
    @property
    def creator(self):
        """
        The creator associated with this application key. Its username is actually returned.

        @rtype: string
        """

        return self._get_field("creator")

    def _show(self, indent = 0):
        super(ApplicationKey, self)._show(indent)
        print " "*indent, "Token:", self.token
        print " "*indent, "Expiration date:", self.expiration_date
        print " "*indent, "Group:", self.group
        print " "*indent, "Creator:", self.creator
