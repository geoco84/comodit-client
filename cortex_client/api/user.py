# coding: utf-8
"""
User module.

@organization: Guardis
@copyright: 2011 Guardis SPRL, Liège, Belgium.
"""

from resource import Resource

class UserFactory(object):
    def new_object(self, json_data):
        return User(None, json_data)

class User(Resource):
    """
    A user's representation.
    """
    def __init__(self, collection, json_data = None):
        """
        @param api: An access point.
        @type api: L{CortexApi}
        @param json_data: A quasi-JSON representation of application's state.
        @type json_data: dict, list or String
        """
        super(User, self).__init__(collection, json_data)

    def get_description(self):
        raise NotImplementedError

    def set_description(self, description):
        raise NotImplementedError

    def get_name(self):
        return self._get_field("username")

    def set_name(self, username):
        return self._set_field("username", username)

    def get_full_name(self):
        return self._get_field("fullname")

    def set_full_name(self, fullname):
        return self._set_field("fullname", fullname)

    def get_email(self):
        return self._get_field("email")

    def set_email(self, email):
        return self._set_field("email", email)

    def get_role(self):
        """
        Provides the role associated to this user.
        @return: A role
        @rtype: String
        """
        return self._get_field("role")

    def set_role(self, role):
        """
        Sets the role associated to this user.
        @param role: A roles
        @type roles: String
        """
        return self._set_field("role", role)

    def _show(self, indent = 0):
        print " "*indent, "Username:", self.get_name()
        print " "*indent, "Full name:", self.get_full_name()
        print " "*indent, "E-mail:", self.get_email()
        print " "*indent, "Role:", self.get_role()

    def dump(self, output_folder):
        raise NotImplementedError

    def load(self, input_folder):
        raise NotImplementedError
