import json
import os


class Storage(object):
    def __init__(self):
        self.path = '/tmp/dao_storage.json'
        self.data = None

    def set(self, key, val):
        self.load()
        self.data[key] = val
        with open(self.path, 'w+') as f:
            json.dump(self.data, f)

    def get(self, key):
        self.load()
        return self.data.get(key)

    def load(self, force=False):
        if not force and self.data is not None:
            return
        try:
            with open(self.path) as f:
                self.data = json.load(f)
        except IOError:
            self.data = {}


store = Storage()
