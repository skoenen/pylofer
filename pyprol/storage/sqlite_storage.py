try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import sqlite3
import os
import re
import sys

from collections import namedtuple
from json import dumps as encode_to_string


__all__ = ['SQLiteStorage']

SCHEME = ('sqlite', 'sqlite3')

TimingTableEntry = namedtuple("TimingTableEntry",
        ["timestamp",
        "name",
        "call_count",
        "recursive_call_count",
        "time_total",
        "time_function",
        "call_stack"])

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
            "call_count INTEGER, "
            "recursive_call_count INTEGER, "
            "time_total REAL, "
            "time_function REAL, "
            "call_stack TEXT)")]

    insert_timing = ("INSERT INTO timings "
                    "(timestamp, measure_point, call_count, "
                    "recursive_call_count, time_total, "
                    "time_function, call_stack) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)")

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
        if hasattr(measure, 'timing'):
            timing_entry = TimingTableEntry(
                    measure.timestamp,
                    measure.name,
                    measure.timing.call_count,
                    measure.timing.recursive_call_count,
                    measure.timing.time_total,
                    measure.timing.time_function,
                    encode_to_string(measure.timing.call_stack))

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

