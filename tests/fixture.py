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
        ["timestamp", "session", "name", "code",
        "call_count", "recursive_call_count", "time_total", "time_function",
        "calls"])

# Just do nothing to measure a function
def nop():
    pass

def timing_stat(name=None, session=None, sub_calls=True, max_tt=None):
    min_time = 0.0000001

    if name is None:
        name = "test"

    if session is None:
        session = name

    call_count = random.randint(1, 100)
    rec_call_count = random.randint(0, call_count-1)

    if max_tt is not None:
        time_total = random.uniform(min_time, max_tt)
    else:
        time_total = random.random()

    time_function = random.uniform(0.0000001, time_total)

    if max_tt is None and sub_calls:
        calls = [timing_stat(name, session, False,
                        (time_total - time_function) /2),
                timing_stat(name, session, False,
                        (time_total - time_function) /2)]
    else:
        calls = None

    return TimingStat(
            datetime.utcnow(), session, name, "test.py", call_count,
            rec_call_count, time_total, time_function, calls)

class Configuration:
    def __init__(self, config=None):
        self.storage_endpoint = urlparse(
                "sqlite://$HOME/pyprol_tests_sqlite_storage")

        self.measure = OptionContainer()
        self.measure.save_process_wait = 0.01

class Measure:
    def __init__(self, session=None, calls=True):
        self.name = "run_test"
        self.timestamp = datetime.utcnow()

        if session is None:
            self.measure_session = self.name
        else:
            self.measure_session = session

        try:
            indexes = xrange(0, 5)
        except NameError:
            indexes = range(0, 5)

        self.timings = list()
        for i in indexes:
            self.timings.append(timing_stat(self.name, self.measure_session,
                    calls))

    def encode_timing_calls(self, calls):
        coded_calls = None
        if calls is not None:
            coded_calls = list()
            for call in calls:
                coded_calls.append(
                        (call.timestamp.isoformat(), self.measure_session,
                        call.name, call.code, call.call_count,
                        call.recursive_call_count, call.time_total,
                        call.time_function, call.calls))

        return json.dumps(coded_calls)

    def to_tuple(self):
        res = list()

        for timing in self.timings:
            res.append(
                    (_str(timing.timestamp.isoformat()),
                    _str(self.measure_session),
                    _str(self.name),
                    _str(timing.code),
                    timing.call_count,
                    timing.recursive_call_count,
                    timing.time_total,
                    timing.time_function,
                    self._calls_tuple(timing)))

        return tuple(res)

    def _calls_tuple(self, timing):
        call_list = list()

        if timing.calls is not None:
            for call in timing.calls:
                call_list.append(
                        (_str(call.timestamp.isoformat()),
                        _str(self.name),
                        _str(call.code),
                        call.call_count,
                        call.recursive_call_count,
                        call.time_total,
                        call.time_function))

        return tuple(call_list)

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

