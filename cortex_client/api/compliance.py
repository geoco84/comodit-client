# coding: utf-8
from cortex_client.api.collection import Collection
from cortex_client.api.resource import Resource
from cortex_client.control.exceptions import ArgumentException
from cortex_client.util.json_wrapper import JsonWrapper

class ServiceState(JsonWrapper):
    def is_running(self):
        return self._get_field("running")

    def is_enabled(self):
        return self._get_field("enabled")

    def show(self, indent = 0):
        print " " * indent, "Running:", self.is_running()
        print " " * indent, "Enabled:", self.is_enabled()

class FileState(JsonWrapper):
    def get_creation_time(self):
        return self._get_field("creationTime")

    def get_group(self):
        return self._get_field("group")

    def get_mode(self):
        return self._get_field("mode")

    def get_modification_time(self):
        return self._get_field("modificationTime")

    def get_owner(self):
        return self._get_field("owner")

    def get_path(self):
        return self._get_field("path")

    def is_present(self):
        return self._get_field("present")

    def show(self, indent = 0):
        print " " * indent, "Present:", self.is_present()
        if self.is_present():
            print " " * indent, "Creation time:", self.get_creation_time()
            print " " * indent, "Modification time:", self.get_modification_time()
            print " " * indent, "Owner:", self.get_owner()
            print " " * indent, "Group:", self.get_group()
            print " " * indent, "Mode:", self.get_mode()

class PackageState(JsonWrapper):
    def is_installed(self):
        return self._get_field("installed")

    def show(self, indent = 0):
        print " " * indent, "Installed:", self.is_installed()

class ComplianceError(Resource):
    def _get_path(self):
        return self._collection.get_path() + self.get_error_collection() + "/" + self.get_id().replace("/", "%2f")

    def get_error_collection(self):
        return self._get_field("collection")

    def set_error_collection(self, collection):
        return self._set_field("collection", collection)

    def get_id(self):
        return self._get_field("id")

    def set_id(self, new_id):
        return self._set_field("id", new_id)

    def get_name(self):
        return self.get_error_collection() + "/" + self.get_id()

    def get_current_state(self):
        return self._get_state("current")

    def get_expected_state(self):
        return self._get_state("expected")

    def _get_state(self, state):
        if self.get_error_collection() == "services":
            return ServiceState(self._get_field(state + "State"))
        elif self.get_error_collection() == "files":
            return FileState(self._get_field(state + "State"))
        elif self.get_error_collection() == "packages":
            return PackageState(self._get_field(state + "State"))
        else:
            return self._get_field("currentState")

    def _show(self, indent = 0):
        col = self.get_error_collection()
        print " " * indent, "Collection:", col
        print " " * indent, "Id:", self.get_id()

        print " " * indent, "Current state:"
        self.get_current_state().show(indent + 2)

        print " " * indent, "Expected state:"
        self.get_expected_state().show(indent + 2)

class ComplianceCollection(Collection):
    def _new_resource(self, json_data):
        return ComplianceError(self, json_data)

    def __split_name(self, name):
        slash_index = name.find("/")
        if slash_index == -1:
            raise ArgumentException("Wrong compliance error name, should be of the form <collection>/<id>")
        return (name[0:slash_index], name[slash_index + 1:])

    def get_resource(self, name):
        (col, e_id) = self.__split_name(name)
        error = ComplianceError(self, None)
        error.set_error_collection(col)
        error.set_id(e_id)
        error.update()
        return error
