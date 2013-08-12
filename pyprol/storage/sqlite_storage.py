try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import sqlite3
import os
import re


__all__ = ['SQLiteStorage']

SCHEME = ('sqlite', 'sqlite3')

class SQLiteStorage(object):
    create_tables = [
            ("CREATE TABLE IF NOT EXISTS timings ("
            "measure_point VARCHAR(255) NOT NULL, "
            "call_count INTEGER, "
            "time_total REAL, "
            "time_in_function REAL, "
            "time_average REAL)"),
             ("CREATE TABLE IF NOT EXISTS memory ("
            "measure_point VARCHAR(255) NOT NULL, "
            "objects_before INTEGER, "
            "objects_after INTEGER, "
            "bytes_before INTEGER, "
            "bytes_after INTEGER, "
            "list_before TEXT, "
            "list_after TEXT "
            ")")]
    insert = "INSERT INTO measures VALUES (?, ?, ?, ?, ?)"

    def __init__(self, config, parsed_url=None):
        self.config = config

        if parsed_url is None:
            parsed_url = urlparse(self.config.storage_endpoint)

        self.conn = sqlite3.connect(parsed_url.netloc + parsed_url.path)
        for create_query in create_tables:
            self.conn.execute(create_query)

    def save(self, measure):
        self.conn.execute(self.insert, measure)

    @classmethod
    def var_expand(self, string):
        for key in os.environ.keys():
            string = re.sub("\${}".format(key), os.environ[key], string)

        return string

