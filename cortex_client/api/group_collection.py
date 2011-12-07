# coding: utf-8

from collection import Collection
from group import Group

class GroupCollection(Collection):
    """
    Application collection. Collection of the applications available in a
    particular organization.
    """

    def __init__(self, api, collection_path):
        super(GroupCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        group = Group(self, json_data)
        return group
