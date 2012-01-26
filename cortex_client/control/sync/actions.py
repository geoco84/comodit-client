from cortex_client.api.host import Host

class Action(object):
    def __init__(self, is_fast_forward):
        self._is_fast_forward = is_fast_forward

    def isFastForward(self):
        return self._is_fast_forward

    def executeAction(self):
        raise NotImplementedError

    def get_summary(self):
        raise NotImplementedError

    def display(self):
        print "Fast-forward:", self._is_fast_forward
        print "Summary: " + self.get_summary()

class UploadContent(Action):
    def __init__(self, src_file, res, file_name):
        super(UploadContent, self).__init__(True)
        self._src_file = src_file
        self._res = res
        self._file_name = file_name

    def get_summary(self):
        return "Upload file " + self._src_file

    def executeAction(self):
        file_res = self._res.files().get_resource(self._file_name)
        file_res.set_content(self._src_file)

class ResourceAction(Action):
    def __init__(self, is_fast_forward, res_object):
        super(ResourceAction, self).__init__(is_fast_forward)
        self._res_object = res_object

    def display(self):
        super(ResourceAction, self).display()
        print "Resource:", self._res_object.__class__.__name__

class UpdateResource(ResourceAction):
    def __init__(self, is_fast_forward, res_object):
        super(UpdateResource, self).__init__(is_fast_forward, res_object)

    def executeAction(self):
        if(isinstance(self._res_object, Host)):
            self._res_object.commit(True)
        else:
            self._res_object.commit(False)

    def get_summary(self):
        return "Update resource " + self._res_object.get_name()

class CreateResource(ResourceAction):
    def __init__(self, is_fast_forward, res_object):
        super(CreateResource, self).__init__(is_fast_forward, res_object)

    def executeAction(self):
        self._res_object.create()

    def get_summary(self):
        return "Create resource " + self._res_object.get_name()

class CreateInstance(ResourceAction):
    def __init__(self, is_fast_forward, host, instance):
        super(CreateInstance, self).__init__(is_fast_forward, host)
        self._instance = instance

    def executeAction(self):
        props = self._instance._get_field("properties")
        if not props is None:
            self._res_object.set_instance_properties(props)

    def get_summary(self):
        return "Create instance for host " + self._res_object.get_name()

class ActionsQueue:
    def __init__(self):
        self._all_fast_forward = True
        self._actions = []

    def addAction(self, action):
        if(not action.isFastForward()):
            self._all_fast_forward = False
        self._actions.append(action)

    def isFastForward(self):
        return self._all_fast_forward

    def executeActions(self):
        for a in self._actions:
            print "-"*80
            print "Executing '" + a.get_summary() + "'"
            a.executeAction()
        print "-"*80

    def display(self):
        for a in self._actions:
            print "-"*80
            a.display()
        print "-"*80
