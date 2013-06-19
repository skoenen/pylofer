import socket
import threading
import json

from storage import FileStorage

__all__ = ['Measurement']

class Measurement(object):
    def __init__(self, config={}, data=None):
        if data:
            obj = json.dumps(data)
            self._merge_with(obj)
        else:
            self.data = {}

        self.config = config
        self.storage = getattr(self.config, "storage", None)
        if not self.storage:
            self.storage = FileStorage()

    def _merge_with(self, obj):
        self.data = obj

    def save(self):
        self.storage.save(self)

    def __str__(self):
        return json.dumps(self.data)

    def __repr__(self):
        return __str__()

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return getattr(self.data, key, None)

    def delitem(self, key):
        if key in self.data:
            del(self.data[key])

