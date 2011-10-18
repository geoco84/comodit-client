from collection import Collection
from directory import Directory
from distribution import Distribution

class DistributionCollection(Collection):
    def __init__(self):
        super(DistributionCollection, self).__init__("distributions")

    def _new_resource(self, json_data):
        return Distribution(json_data)

    def get_uuid(self, path):
        return Directory.get_distribution_uuid(path)
