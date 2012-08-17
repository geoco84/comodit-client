from cortex_client.api.collection import Collection
from cortex_client.api.resource import Resource

class AppStoreCollection(Collection):
    def __init__(self, api):
        super(AppStoreCollection, self).__init__("store/applications/", api)

    def _new_resource(self, json_data):
        return PublishedApplication(self, json_data)

class DistStoreCollection(Collection):
    def __init__(self, api):
        super(DistStoreCollection, self).__init__("store/distributions/", api)

    def _new_resource(self, json_data):
        return PublishedDistribution(self, json_data)

class PublishedEntity(Resource):
    def __init__(self, collection, json_data = None):
        super(PublishedEntity, self).__init__(collection, json_data)

    def get_identifier(self):
        return self.get_uuid()

    def _get_path(self):
        return self._collection.get_path() + self.get_uuid() + "/"

    def get_label(self):
        return self.get_name()

    def get_name(self):
        return self._get_field("name")

    def get_description(self):
        return self._get_field("description")

    def get_author(self):
        return self._get_field("author")

    def get_publisher(self):
        return self._get_field("publisher")

    def get_publishing_organization(self):
        return self._get_field("publishingOrganization")

    def get_published_version(self):
        return self._get_field("publishedVersion")

    def get_date_published(self):
        return self._get_field("datePublished")

    def get_date_updated(self):
        return self._get_field("dateUpdated")

    def get_url(self):
        return self._get_field("url")

class PublishedApplication(PublishedEntity):
    def __init__(self, collection, json_data = None):
        super(PublishedApplication, self).__init__(collection, json_data)

    def get_application(self):
        return self._get_field("application")

class PublishedApplicationFactory(object):
    def __init__(self, collection = None):
        self._collection = collection

    def new_object(self, json_data):
        return PublishedApplicationFactory(self._collection, json_data)

class PublishedDistribution(PublishedEntity):
    def __init__(self, collection, json_data = None):
        super(PublishedDistribution, self).__init__(collection, json_data)

    def get_distribution(self):
        return self._get_field("distribution")

class PublishedDistributionFactory(object):
    def __init__(self, collection = None):
        self._collection = collection

    def new_object(self, json_data):
        return PublishedDistribution(self._collection, json_data)
