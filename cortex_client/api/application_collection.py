from collection import Collection
from directory import Directory
from application import Application

class ApplicationCollection(Collection):
    def __init__(self):
        super(ApplicationCollection, self).__init__("applications")

    def _new_resource(self, json_data):
        return Application(json_data)

    def get_uuid(self, path):
        return Directory.get_application_uuid(path)
