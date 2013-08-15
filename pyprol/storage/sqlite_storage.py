try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import sqlite3
import os
import re

from collections import namedtuple


__all__ = ['SQLiteStorage']

SCHEME = ('sqlite', 'sqlite3')

TimingTableEntry = namedtuple("TimingTableEntry",
        ["name", "call_count", "time_total", "time_in_function", "call_stack"])

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
            "time_total REAL, "
            "time_in_function REAL, "
            "call_stack TEXT)"),
             ("CREATE TABLE IF NOT EXISTS memory ("
            "timestamp TEXT, "
            "measure_point VARCHAR(255) NOT NULL, "
            "objects_before INTEGER, "
            "objects_after INTEGER, "
            "bytes_before INTEGER, "
            "bytes_after INTEGER, "
            "list_before TEXT, "
            "list_after TEXT)")]
    insert_timing = ("INSERT INTO timings "
                    "(timestamp, measure_point, call_count, time_total, "
                    "time_in_function, call_stack) "
                    "VALUES (?, ?, ?, ?, ?, ?)")
    insert_memory = ("INSERT INTO memory "
                    "(measure_point, objects_before, objects_after,"
                    " bytes_before, bytes_after, list_before, list_after) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)")

    conn = None

    def __init__(self, config):
        self.config = config
        path = SQLiteStorage.var_expand(self.config.storage_endpoint.netloc)
        path += SQLiteStorage.var_expand(self.config.storage_endpoint.path)

        try:
            self.conn = sqlite3.connect(path)
        except sqlite3.OperationalError:
            raise RuntimeError(
                    "Can not open pyprol sqlite database '{}'".format(path))

        for create_query in self.create_tables:
            self.conn.execute(create_query)

        self.conn.commit()

    def save(self, measure):
        if hasattr(measure, 'timing'):
            timing_entry = TimingTableEntry(
                    measure.timestamp,
                    measure.name,
                    *measure.timings)
            self.conn.execute(self.insert_timing, timing_entry)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    @classmethod
    def var_expand(self, string):
        for key in os.environ.keys():
            string = re.sub("\${}".format(key), os.environ[key], string)

        return string

