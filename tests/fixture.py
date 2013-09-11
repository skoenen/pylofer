from collections import namedtuple
from datetime import datetime
from multiprocessing import Manager

import random
import json

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

try:
    _str = unicode
except NameError:
    _str = str

TimingStat = namedtuple(
        "TimingStat",
        ["timestamp", "name", "code", "call_count", "recursive_call_count",
        "time_total", "time_function", "calls"])

# Just do nothing to measure a function
def nop():
    pass

def timing_stat(name=None, max_call=None, max_tt=None):
    min_time = 0.0000001

    if name is None:
        name = "test"

    if max_call is not None:
        call_count = random.randint(1, max_call)
    else:
        call_count = random.randint(1, 100)

    rec_call_count = random.randint(0, call_count-1)

    if max_tt is not None:
        time_total = random.uniform(min_time, max_tt)
    else:
        time_total = random.random()

    time_function = random.uniform(0.0000001, time_total)

    if max_call is None:
        calls = [timing_stat(name,
                        call_count -1, (time_total - time_function) /2),
                timing_stat(name,
                        call_count -2, (time_total - time_function) /2)]
    else:
        calls = None

    return TimingStat(
            datetime.utcnow(), name, "test.py", call_count, rec_call_count,
            time_total, time_function, calls)

class Configuration:
    def __init__(self, config=None):
        self.storage_endpoint = urlparse(
                "sqlite://$HOME/pyprol_tests_sqlite_storage")

        self.measure = OptionContainer()
        self.measure.save_process_wait = 0.01

class Measure:
    def __init__(self):
        self.name = "run_test"
        self.timestamp = datetime.utcnow()

        try:
            indexes = xrange(0, 5)
        except NameError:
            indexes = range(0, 5)

        self.timings = list()
        for i in indexes:
            self.timings.append(timing_stat(self.name))

    def to_db_repr(self):
        timing_list = list()

        for timing in self.timings:
            timing_list.append(
                    (_str(timing.timestamp.isoformat()),
                    _str(self.name), _str(timing.code),
                    timing.call_count, timing.recursive_call_count,
                    timing.time_total,
                    timing.time_function,
                    _str(json.dumps(timing.calls))))

        return timing_list


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

