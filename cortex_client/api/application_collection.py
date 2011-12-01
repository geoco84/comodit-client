# coding: utf-8
"""
Application collection module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from collection import Collection
from application import Application

class ApplicationCollection(Collection):
    """
    Application collection. Collection of the applications available in a
    particular organization.
    """

    def __init__(self, api, collection_path):
        """
        Creates a new ApplicationCollection instance.
        
        @param api: Access point to a server
        @type api: L{CortexApi}
        @param collection_path: The path to collection
        @type collection_path: L{String}
        """
        super(ApplicationCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        """
        Instantiates a new Application object with given state.

        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict

        @see: L{Application}
        """
        app = Application(self, json_data)
        return app
