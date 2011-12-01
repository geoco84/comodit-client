# coding: utf-8
"""
Platform collection module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from collection import Collection
from platform import Platform

class PlatformCollection(Collection):
    """
    Platform collection. Collection of the platforms available on a
    cortex server.
    """

    def __init__(self, api, collection_path):
        """
        Creates a new PlatformCollection instance.
        
        @param api: Access point to a server
        @type api: L{CortexApi}
        @param collection_path: The path to collection
        @type collection_path: L{String}
        """
        super(PlatformCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        """
        Instantiates a new Platform object with given state.

        @param json_data: A quasi-JSON representation of Platform's state.
        @type json_data: dict

        @see: L{Platform}
        """

        return Platform(self, json_data)
