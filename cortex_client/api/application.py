from cortex_client.util.json_wrapper import JsonWrapper
from resource import Resource

class ApplicationResource(JsonWrapper):
    def __init__(self, json_data):
        super(ApplicationResource, self).__init__(json_data)

    def get_name(self):
        return self._get_field("name")

    def set_name(self, name):
        return self._set_field("name", name)

    def show(self, indent = 0):
        print " "*indent, self.get_name()


class Package(ApplicationResource):
    pass


class Service(ApplicationResource):
    def get_running(self):
        return self._get_field("running")

    def get_enabled(self):
        return self._get_field("enabled")

    def show(self, indent = 0):
        print " "*indent, self.get_name()+":"
        print " "*(indent+2), "enabled:", self.get_enabled()
        print " "*(indent+2), "running", self.get_running()


class File(ApplicationResource):
    def get_owner(self):
        return self._get_field("owner")

    def get_group(self):
        return self._get_field("group")

    def get_mode(self):
        return self._get_field("mode")

    def get_path(self):
        return self._get_field("path")

    def get_template_uuid(self):
        return self._get_field("template")

    def show(self, indent = 0):
        print " "*indent, self.get_name()+":"
        print " "*(indent+2), "owner:", self.get_owner()
        print " "*(indent+2), "group:", self.get_group()
        print " "*(indent+2), "mode:", self.get_mode()
        print " "*(indent+2), "path:", self.get_path()
        print " "*(indent+2), "template:", self.get_template_uuid()


class Action(JsonWrapper):
    def __init__(self, json_data):
        super(Action, self).__init__(json_data)

    def get_type(self):
        return self._get_field("action")

    def get_resource(self):
        return self._get_field("resource")

    def show(self, indent = 0):
        print self.get_type(), self.get_resource()

class Handler(JsonWrapper):
    def __init__(self, json_data):
        super(Handler, self).__init__(json_data)

    def get_actions(self):
        actions_json = self._get_field("do")
        actions = []
        if(actions_json):
            for a in actions_json:
                actions.append(Action(a))
        return actions

    def set_actions(self, actions):
        json_actions = []
        for a in actions:
            json_actions.append(a.get_json())
        self._set_field("do", json_actions)

    def get_triggers(self):
        actions_json = self._get_field("on")
        actions = []
        if(actions_json):
            for a in actions_json:
                actions.append(a)
        return actions

    def set_triggers(self, triggers):
        json_triggers = []
        for t in triggers:
            json_triggers.append(t)
        self._set_field("on", json_triggers)

    def show(self, indent = 0):
        print "Actions:"
        actions = self.get_actions()
        for a in actions:
            a.show(indent + 2)
        print "Triggers:"
        triggers = self.get_triggers()
        for t in triggers:
            print " "*(indent + 2), t


class Application(Resource):
    def __init__(self, json_data = None):
        from application_collection import ApplicationCollection
        super(Application, self).__init__(ApplicationCollection(), json_data)

    def get_packages(self):
        packages = []
        json_packages = self._get_field("packages")
        if(json_packages):
            for s in json_packages:
                packages.append(Package(s))
        return packages

    def set_packages(self, packages):
        json_packages = []
        for p in packages:
            json_packages.append(p.get_json())
        self._set_field("packages", json_packages)

    def get_services(self):
        packages = []
        json_packages = self._get_field("services")
        if(json_packages):
            for s in json_packages:
                packages.append(Service(s))
        return packages

    def set_services(self, services):
        json_packages = []
        for p in services:
            json_packages.append(p.get_json())
        self._set_field("services", json_packages)

    def get_files(self):
        packages = []
        json_packages = self._get_field("files")
        if(json_packages):
            for s in json_packages:
                packages.append(File(s))
        return packages

    def set_files(self, services):
        json_packages = []
        for p in services:
            json_packages.append(p.get_json())
        self._set_field("files", json_packages)

    def get_handlers(self):
        packages = []
        json_packages = self._get_field("handlers")
        if(json_packages):
            for s in json_packages:
                packages.append(Handler(s))
        return packages

    def set_handlers(self, services):
        json_packages = []
        for p in services:
            json_packages.append(p.get_json())
        self._set_field("handlers", json_packages)

    def _show(self, indent = 0):
        print " "*indent, "UUID:", self.get_uuid()
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Packages:"
        packages = self.get_packages()
        for p in packages:
            p.show(indent + 2)
        print " "*indent, "Services:"
        services = self.get_services()
        for s in services:
            s.show(indent + 2)
        print " "*indent, "Files:"
        files = self.get_files()
        for f in files:
            f.show(indent + 2)
        print " "*indent, "Handlers:"
        handlers = self.get_handlers()
        for f in handlers:
            f.show(indent + 2)