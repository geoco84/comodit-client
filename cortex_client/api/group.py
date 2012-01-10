# coding: utf-8

from resource import Resource
from cortex_client.api.user import UserFactory

class Group(Resource):
    def __init__(self, collection, json_data = None):
        super(Group, self).__init__(collection, json_data)

    def get_name(self):
        return self._get_field("name")

    def get_description(self):
        return self._get_field("description")

    def set_description(self, desc):
        return self._set_field("description", desc)

    def get_organization(self):
        return self._get_field("organization")

    def get_uuid(self):
        return self._get_field("uuid")

    def get_users(self):
        return self._get_list_field("users", UserFactory())

    def add_user(self, user):
        return self._add_to_list_field("users", user)

    def remove_user(self, user):
        users = self._get_field("users")
        users.remove(user)

    def clear_users(self, user):
        return self._set_list_field("users", [])

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Organization:", self.get_organization()
        print " "*indent, "Users:"
        users = self.get_users()
        for u in users:
            print " "*(indent + 2), "Username:", u.get_name()
            print " "*(indent + 2), "Full name:", u.get_full_name()
            print " "*(indent + 2), "E-mail:", u.get_email()
            print
