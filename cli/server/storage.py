import json
import os


class Storage(object):
    def __init__(self):
        self.path = '/tmp/dao_storage.json'
        self.data = {}
        if os.path.isfile(self.path):
            with open(self.path) as f:
                self.data = json.load(f)

    def set(self, key, val):
        self.data[key] = val
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def get(self, key):
        return self.data.get(key)

store = Storage()