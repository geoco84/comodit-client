# coding: utf-8
"""
Distribution collection module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from collection import Collection
from distribution import Distribution

class DistributionCollection(Collection):
    """
    Distribution collection. Collection of the distributions available on a
    cortex server.
    """

    def __init__(self, api, collection_path):
        """
        Creates a new DistributionCollection instance.
        
        @param api: Access point to a server
        @type api: L{CortexApi}
        @param collection_path: The path to collection
        @type collection_path: L{String}
        """
        super(DistributionCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        """
        Instantiates a new Distribution object with given state.

        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict

        @see: L{Distribution}
        """

        return Distribution(self, json_data)
