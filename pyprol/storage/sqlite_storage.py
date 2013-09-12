try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import sqlite3
import os
import re
import sys
import json

from collections import namedtuple


__all__ = ['SQLiteStorage']

SCHEME = ('sqlite', 'sqlite3')

TimingTableEntry = namedtuple("TimingTableEntry",
        ["timestamp", "name", "code", "call_count", "recursive_call_count",
        "time_total", "time_function", "calls"])

def encode_timing_stat_calls(calls):
    coded_calls = None
    if calls is not None:
        coded_calls = list()
        for call in calls:
            coded_calls.append(
                    (call.timestamp.isoformat(), call.name, call.code,
                    call.call_count, call.recursive_call_count, call.time_total,
                    call.time_function, call.calls))

    return json.dumps(coded_calls)

class SQLiteStorage(object):
    """ Storage implementation to save measure values in a sqlite database.

        URL:
            SCHEME:         PATH
            sqlite://       <sqlite db file path>

        PATH:
            In this section the environment variables will be expanded, like
            $HOME
    """

    create_tables = [
            ("CREATE TABLE IF NOT EXISTS timings ("
            "timestamp TEXT, "
            "measure_point VARCHAR(255) NOT NULL, "
            "code VARCHAR(255) NOT NULL, "
            "call_count INTEGER, "
            "recursive_call_count INTEGER, "
            "time_total REAL, "
            "time_function REAL, "
            "calls TEXT)")]

    insert_timing = ("INSERT INTO timings "
                    "(timestamp, measure_point, code, call_count, "
                    "recursive_call_count, time_total, "
                    "time_function, calls) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

    def __init__(self, config):
        self.config = config
        path = var_expand(self.config.storage_endpoint.netloc)
        path += var_expand(self.config.storage_endpoint.path)

        try:
            self.conn = sqlite3.connect(path)
        except sqlite3.OperationalError:
            _, error, _ = sys.exc_info()
            raise RuntimeError(
                    ("Can not open pyprol sqlite database '{0}', "
                    "because of '{1}'").format(path, error))

        for create_query in self.create_tables:
            self.conn.execute(create_query)

        self.conn.commit()

    def save(self, measure):
        if hasattr(measure, 'timings'):
            for timing in measure.timings:
                timing_entry = TimingTableEntry(
                        timing.timestamp.isoformat(),
                        timing.name,
                        timing.code,
                        timing.call_count,
                        timing.recursive_call_count,
                        timing.time_total,
                        timing.time_function,
                        encode_timing_stat_calls(timing.calls))

                self.conn.execute(self.insert_timing, timing_entry)
            self.conn.commit()

    def close(self):
        if hasattr(self, "conn"):
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

def var_expand(string):
    return re.sub(r"\$([A-Z_0-9]+[A-Z0-9])", lambda m: os.environ[m.group(1)], string)

IMPL = SQLiteStorage

