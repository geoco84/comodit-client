# coding: utf-8
"""
Host collection module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from collection import Collection

class HostCollection(Collection):
    """
    Host collection. Collection of the hosts available on a
    cortex server.
    """

    def __init__(self, api, collection_path):
        """
        Creates a new HostCollection instance.
        
        @param api: Access point to a server
        @type api: L{CortexApi}
        @param collection_path: The path to collection
        @type collection_path: L{String}
        """
        super(HostCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        """
        Instantiates a new Host object with given state.

        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict

        @see: L{Host}
        """

        from host import Host
        return Host(self, json_data)
