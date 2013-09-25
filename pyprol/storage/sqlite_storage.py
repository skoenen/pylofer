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
from logging import getLogger


__all__ = ['SQLiteStorage']

log = getLogger(__name__)

SCHEME = ('sqlite', 'sqlite3')

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
            "measure_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "timestamp TEXT NOT NULL, "
            "measure_session VARCHAR(255) NOT NULL, "
            "measure_point VARCHAR(255) NOT NULL, "
            "code VARCHAR(255) NOT NULL, "
            "call_count INTEGER, "
            "recursive_call_count INTEGER, "
            "time_total REAL, "
            "time_function REAL)"),

            ("CREATE TABLE IF NOT EXISTS timings_calls ("
            "measure_id INTEGER NOT NULL,"
            "timestamp TEXT NOT NULL, "
            "measure_point VARCHAR(255) NOT NULL, "
            "code VARCHAR(255) NOT NULL, "
            "call_count INTEGER, "
            "recursive_call_count INTEGER, "
            "time_total REAL, "
            "time_function REAL, "
            "FOREIGN KEY (measure_id) REFERENCES "
            "timings (measure_id)) ")]
            #"ON DELETE CASCADE "
            #"ON UPDATE CASCADE)")]

    insert_timing = ("INSERT INTO timings "
                    "(timestamp, measure_session, measure_point, code, "
                    "call_count, recursive_call_count, time_total, "
                    "time_function) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

    insert_subcall = ("INSERT INTO timings_calls "
                     "(measure_id, timestamp, measure_point, code, "
                     "call_count, recursive_call_count, time_total, "
                     "time_function) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

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
        log.debug("Measure to save: {}".format(measure))
        if hasattr(measure, 'timings'):
            for timing in measure.timings:
                cursor = self.conn.cursor()
                timing_entry = (
                        timing.timestamp.isoformat(),
                        timing.session,
                        timing.name,
                        timing.code,
                        timing.call_count,
                        timing.recursive_call_count,
                        timing.time_total,
                        timing.time_function)

                cursor.execute(self.insert_timing, timing_entry)
                measure_id = cursor.lastrowid

                if timing.calls is not None:
                    for call in timing.calls:
                        timing_call = (
                                measure_id,
                                call.timestamp.isoformat(),
                                call.name,
                                call.code,
                                call.call_count,
                                call.recursive_call_count,
                                call.time_total,
                                call.time_function)

                        cursor.execute(self.insert_subcall, timing_call)
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

