from collections import namedtuple
from datetime import datetime

import random
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


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

class StorageFactory:
    pass

class Storage:
    pass

