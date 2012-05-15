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
        return self._collection.get_path() + self.get_name()

    def get_application(self):
        return self._get_field("application")

    def set_application(self, app):
        return self._set_field("application", app)

    def get_resource_type(self):
        return self._get_field("type")

    def set_resource_type(self, type):
        return self._set_field("type", type)

    def get_type_collection(self):
        res_type = self.get_resource_type()
        if res_type == "serviceResource":
            return "services"
        elif res_type == "fileResource":
            return "files"
        elif res_type == "packageResource":
            return "packages"

    def set_type_collection(self, col):
        if col == "services":
            self.set_resource_type("serviceResource")
        elif col == "files":
            self.set_resource_type("fileResource")
        elif col == "packages":
            self.set_resource_type("packageResource")

    def get_res_name(self):
        return self._get_field("name")

    def set_res_name(self, name):
        return self._set_field("name", name)

    def get_name(self):
        return "applications/" + self.get_application() + "/" + self.get_type_collection() + "/" + self.get_res_name()

    def get_current_state(self):
        return self._get_state("current")

    def get_expected_state(self):
        return self._get_state("expected")

    def _get_state(self, state):
        if self.get_resource_type() == "serviceResource":
            return ServiceState(self._get_field(state + "State"))
        elif self.get_resource_type() == "fileResource":
            return FileState(self._get_field(state + "State"))
        elif self.get_resource_type() == "packageResource":
            return PackageState(self._get_field(state + "State"))
        else:
            return self._get_field("currentState")

    def _show(self, indent = 0):
        col = self.get_resource_type()
        print " " * indent, "Type:", col
        print " " * indent, "Application:", self.get_application()
        print " " * indent, "Name:", self.get_res_name()

        print " " * indent, "Current state:"
        self.get_current_state().show(indent + 2)

        print " " * indent, "Expected state:"
        self.get_expected_state().show(indent + 2)

class ComplianceCollection(Collection):
    def _new_resource(self, json_data):
        return ComplianceError(self, json_data)

    def __split_name(self, name):
        slash_index0 = name.find("/")
        slash_index1 = name.find("/", slash_index0 + 1)
        if slash_index1 == -1:
            raise ArgumentException("Wrong compliance error name, should be of the form applications/<app_name>/<type>/<id>")
        slash_index2 = name.find("/", slash_index1 + 1)
        if slash_index2 == -1:
            raise ArgumentException("Wrong compliance error name, should be of the form applications/<app_name>/<type>/<id>")
        return (name[slash_index0 + 1:slash_index1], name[slash_index1 + 1:slash_index2], name[slash_index2 + 1:])

    def get_resource(self, name):
        (app_name, res_type, res_name) = self.__split_name(name)
        error = ComplianceError(self, None)
        error.set_application(app_name)
        error.set_type_collection(res_type)
        error.set_name(res_name)
        error.update()
        return error
