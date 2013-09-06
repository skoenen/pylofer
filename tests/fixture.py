from collections import namedtuple
from datetime import datetime
from multiprocessing import Manager

import random

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

__all__ = [
        'Configuration',
        'Measure',
        'OptionContainer',
        'StorageFactory',
        'Storage',
        'TimingStat',
        'timing_stat']

TimingStat = namedtuple(
        "TimingStat",
        ["code", "call_count", "recursive_call_count",
        "time_total", "time_function", "call_stack"])

# Just do nothing
def nop():
    pass

def timing_stat():
    call_count = random.randint(1, 100)
    rec_call_count = random.randint(0, call_count-1)
    time_total = random.random()
    time_function = random.uniform(0.0000001, time_total)
    return TimingStat(
            "test.py",
            call_count,
            rec_call_count,
            time_total,
            time_function,
            ["test", "test"])

class Configuration:
    def __init__(self, config=None):
        self.storage_endpoint = urlparse(
                "sqlite://$HOME/pyprol_tests_sqlite_storage")

        self.measure = OptionContainer()
        self.measure.save_process_wait = 0.01

class Measure:
    name = "run_test"
    timestamp = datetime.utcnow()
    timing = timing_stat()

class OptionContainer:
    pass

class MemStorage:
    def __init__(self, config):
        self.config = config
        self.measures = Manager().list()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def save(self, measure):
        self.measures.append(measure)

    def last(self):
        if len(self.measures) <= 0:
            return None

        return self.measures[-1]

    def __str__(self):
        buf = "<{} measures: [".format(self.__class__)
        for item in self.measures:
            buf += "'{}'".format(item)
        buf += "]>"

        return buf

class Storage(object):
    _storage = None

    def __new__(cls, config=None):
        if cls._storage is None:
            cls._storage = MemStorage(config)
        return cls._storage

    def __getattr__(self, name):
        return getattr(self.__dict__['_storage'], name)

    def __setattr__(self, name, val):
        return setattr(self.__dict__['_storage'], name, val)

