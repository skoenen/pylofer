try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import sqlite3


__all__ = ['SQLiteStorage']

SCHEME = ('sqlite', 'sqlite3')

class SQLiteStorage(object):
    create_table = ("CREATE TABLE IF NOT EXISTS measures ("
            "measure_point VARCHAR(255), "
            "call_count INTEGER, "
            "time_total REAL, "
            "time_in_function REAL, "
            "time_average REAL)")
    insert = "INSERT INTO measures VALUES (?, ?, ?, ?, ?)"

    def __init__(self, config, parsed_url=None):
        self.config = config

        if parsed_url is None:
            parsed_url = urlparse(self.config.storage_endpoint)

        self.conn = sqlite3.connect(parsed_url.netloc + parsed_url.path)
        self.conn.execute(self.create_table)

    def save(self, measure):
        self.conn.execute(self.insert, measure)

