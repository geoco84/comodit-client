from collection import Collection
from change_request import *
from exceptions import PythonApiException

class ChangeRequestCollection(Collection):
    def __init__(self):
        super(ChangeRequestCollection, self).__init__("changes")

    def _new_resource(self, json_data):
        if(not json_data.has_key("action")):
            raise PythonApiException("Given JSON is not a change request")

        action = json_data["action"]
        if(action == InstallApplicationChangeRequest.ACTION):
            return InstallApplicationChangeRequest(json_data)
        elif (action == UninstallApplicationChangeRequest.ACTION):
            return UninstallApplicationChangeRequest(json_data)
        elif (action == AddSettingChangeRequest.ACTION):
            return AddSettingChangeRequest(json_data)
        elif (action == UpdateSettingChangeRequest.ACTION):
            return UpdateSettingChangeRequest(json_data)
        elif (action == DeleteSettingChangeRequest.ACTION):
            return DeleteSettingChangeRequest(json_data)

        raise PythonApiException("Unknown change request type: "+action)

    def get_uuid(self, path):
        return path
