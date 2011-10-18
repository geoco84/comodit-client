from collection import Collection
from directory import Directory
from user import User

class UserCollection(Collection):
    def __init__(self):
        super(UserCollection, self).__init__("users")

    def _new_resource(self, json_data):
        return User(json_data)

    def get_uuid(self, path):
        return Directory.get_user_uuid(path)
