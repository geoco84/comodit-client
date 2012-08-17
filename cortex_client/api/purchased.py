from cortex_client.api.collection import Collection
from cortex_client.api.resource import Resource

class PurchasedCollection(Collection):
    def _new_resource(self, json_data):
        return PurchasedEntity(self, json_data)

class PurchasedEntity(Resource):
    def __init__(self, collection, json_data = None):
        super(PurchasedEntity, self).__init__(collection, json_data)

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

    def get_purchased_version(self):
        return self._get_field("purchasedVersion")

    def get_date_purchased(self):
        return self._get_field("datePurchased")

class PublishedEntityFactory(object):
    def __init__(self, collection = None):
        self._collection = collection

    def new_object(self, json_data):
        return PurchasedEntity(self._collection, json_data)
