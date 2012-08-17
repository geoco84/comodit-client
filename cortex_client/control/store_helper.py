import json, os

from cortex_client.control.doc import ActionDoc
from cortex_client.api.exceptions import PythonApiException
from cortex_client.config import Config
from cortex_client.util.editor import edit_text

class StoreHelper(object):
    def __init__(self, ctrl, content_type):
        self._ctrl = ctrl
        self._content_type = content_type
        if content_type == "app":
            self._params = "<org_name> <app_name>"
            self._template = "published_application.json"
            self._type_name = "Application"
            self._label = "application"
        elif content_type == "dist":
            self._params = "<org_name> <dist_name>"
            self._template = "published_distribution.json"
            self._type_name = "Distribution"
            self._label = "distribution"
        else:
            raise PythonApiException("Unhandled type: " + str(content_type))

    def get_store(self):
        if self._content_type == "app":
            return self._ctrl._api.app_store()
        elif self._content_type == "dist":
            return self._ctrl._api.dist_store()
        else:
            return None

    def get_purchased(self, org):
        if self._content_type == "app":
            return org.purchased_apps()
        elif self._content_type == "dist":
            return org.purchased_dists()
        else:
            return None

    def _publish(self, argv):
        app = self._ctrl._get_resource(argv)

        if not app.get_published_as() is None:
            raise PythonApiException(self._type_name + " has already been published")

        template_json = json.load(open(os.path.join(Config()._get_templates_path(), self._template)))
        template_json[self._label] = app.get_uuid()
        updated = edit_text(json.dumps(template_json, indent = 4))

        pub_app = self.get_store()._new_resource(json.loads(updated))
        self.get_store().add_resource(pub_app)

    def _publish_doc(self):
        return ActionDoc("publish", self._params, """
        Publish """ + self._label + """ to store.""")

    def _unpublish(self, argv):
        app = self._ctrl._get_resource(argv)

        if app.get_published_as() is None:
            raise PythonApiException(self._type_name + " is not published")

        self.get_store().get_resource(app.get_published_as()).delete()

    def _unpublish_doc(self):
        return ActionDoc("unpublish", self._params, """
        Unpublish """ + self._label + """ from store.""")

    def _push(self, argv):
        app = self._ctrl._get_resource(argv)

        if app.get_published_as() is None:
            raise PythonApiException(self._type_name + " is not published")

        pub_app = self.get_store()._new_resource({"uuid" : app.get_published_as()})
        pub_app.commit()

    def _push_doc(self):
        return ActionDoc("push", self._params, """
        Push """ + self._label + """ update to store.""")

    def _pull(self, argv):
        app = self._ctrl._get_resource(argv)

        if app.get_purchased_as() is None:
            raise PythonApiException(self._type_name + " is not purchased")

        org = self._ctrl._api.organizations().get_resource(app.get_organization())

        pur = self.get_purchased(org)._new_resource({"uuid" : app.get_purchased_as()})
        pur.commit()

    def _pull_doc(self):
        return ActionDoc("pull", self._params, """
        Pull """ + self._label + """ update from store.""")
