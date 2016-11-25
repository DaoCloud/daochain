import json

from settings import in_data_dir


class Storage(object):
    def __init__(self):
        self.path = in_data_dir('dao_storage.json')
        self.data = None

    def has(self, key):
        self.load()
        return key in self.data

    def set(self, key, val):
        self.load()
        self.data[key] = val
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def delete(self, key):
        self.load()
        if key in self.data:
            del self.data[key]
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def get(self, key, default=None):
        self.load()
        return self.data.get(key, default)

    def load(self, force=False):
        if not force and self.data is not None:
            return
        try:
            with open(self.path) as f:
                self.data = json.load(f)
        except (IOError, ValueError):
            self.data = {}
            with open(self.path, 'w') as f:
                json.dump(self.data, f)


store = Storage()


class Cache(object):
    path = '/tmp/dao_cache.json'

    def __init__(self):
        self.data = None

    @classmethod
    def init(cls):
        with open(cls.path, 'w'):
            pass

    def has(self, key):
        self.load()
        return key in self.data

    def set(self, key, val):
        self.load()
        self.data[key] = val
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def delete(self, key):
        self.load()
        if key in self.data:
            del self.data[key]
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def get(self, key, default=None):
        self.load()
        return self.data.get(key, default)

    def load(self, force=False):
        if not force and self.data is not None:
            return
        try:
            with open(self.path) as f:
                self.data = json.load(f)
        except (IOError, ValueError):
            self.data = {}
            with open(self.path, 'w') as f:
                json.dump(self.data, f)
