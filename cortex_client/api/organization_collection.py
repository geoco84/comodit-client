# coding: utf-8
"""
Organization collection module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from collection import Collection
from organization import Organization

class OrganizationCollection(Collection):
    """
    Organization collection. Collection of the organizations available on a
    cortex server.
    """

    def __init__(self, api):
        """
        Creates a new OrganizationCollection instance.
        
        @param api: Access point to a server
        @type api: L{CortexApi}
        """
        super(OrganizationCollection, self).__init__("organizations/", api)

    def _new_resource(self, json_data):
        """
        Instantiates a new Organization object with given state.

        @param json_data: A quasi-JSON representation of organization's state.
        @type json_data: dict

        @see: L{Organization}
        """

        return Organization(self, json_data)
