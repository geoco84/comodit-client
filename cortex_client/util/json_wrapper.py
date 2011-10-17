import json

class JsonWrapper(object):
    def __init__(self, json_data = None):
        if(json_data):
            self.__json_data = json_data
        else:
            self.__json_data = {}

    def _get_field(self, field):
        if(self.__json_data.has_key(field)):
            return self.__json_data[field]
        else:
            return None

    def _set_field(self, field, value):
        self.__json_data[field] = value

    def set_json(self, json_data):
        self.__json_data = json_data

    def get_json(self):
        return self.__json_data
    
    def print_json(self):
        print json.dumps(self.__json_data)