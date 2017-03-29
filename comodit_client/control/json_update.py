import json
from collections import OrderedDict
from comodit_client.util.editor import edit_text

class JsonUpdater(object):

    def __init__(self, options):
        self._options = options

    def update(self, json_data):
        if self._options.filename:
            with open(self._options.filename, 'r') as f:
                return json.load(f, object_pairs_hook=OrderedDict)
        elif self._options.json:
            return json.loads(self._options.json, object_pairs_hook=OrderedDict)
        else:
            original = json_data.get_real_json(indent = 4)
            updated = edit_text(original)
            return json.loads(updated, object_pairs_hook=OrderedDict)
