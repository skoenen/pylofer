import socket
import threading
import json

__all__ = ['Measurement']

class Measurement(object):
    def __init__(self, config={}, data=None):
        if data:
            obj = json.dumps(data)
            self._merge_with(obj)
        else:
            self.data = {}
            self.typ = "GENERIC"

        self.config = config

    def _merge_with(self, obj):
        if "typ" in obj:
            self.typ = getattr(obj, "typ", "GENERIC")
            del obj["typ"]

        self.data = obj

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

class TimingMeasurement(Measurement):
    def __init__(self, config={}, data=None):
        super(TimingMeasurement, self).__init__(config, data)
        self.typ = "TIMING"
