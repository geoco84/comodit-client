# coding: utf-8
"""
Environment collection module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from collection import Collection
from environment import Environment

class EnvironmentCollection(Collection):
    """
    Environment collection. Collection of the environments available on a
    cortex server.
    """

    def __init__(self, api, collection_path):
        """
        Creates a new EnvironmentCollection instance.
        
        @param api: Access point to a server
        @type api: L{CortexApi}
        @param collection_path: The path to collection
        @type collection_path: L{String}
        """
        super(EnvironmentCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        """
        Instantiates a new Environment object with given state.

        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict

        @see: L{Environment}
        """

        return Environment(self, json_data)
