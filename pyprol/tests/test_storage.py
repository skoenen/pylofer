from unittest import TestCase
from datetime import date
from collections import namedtuple

import os

#from storage.server_storage import ServerStorage
from storage import sqlite_storage
#from storage.console_storage import ConsoleStorage
#from storage.file_storage import FileStorage
from storage.factory import StorageFactory

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Configuration:
    pass

class Measure:
    timings = None

TimingStat = namedtuple(
        "TimingStat",
        ["call_count", "time_total", "time_in", "calls"])

#class ServerStorageTestCase(TestCase):

    #def setUp(self):
        #self.config = Configuration()

    #def test_udp(self):
        #self.config[endpoint] = "udp://127.0.0.1:65333"

        #parsed = urlparse(self.config.storage_endpoint)
        #storage = ServerStorage(self.config, parsed)

    #def test_udp6(self):
        #self.config[endpoint] = "udp6://[::1]:65333"

        #parsed = urlparse(self.config.storage_endpoint)
        #storage = ServerStorage(self.config, parsed)

    #def test_unix(self):
        #self.config[endpoint] = "unix:///var/run/pyprol.server.socket"

        #parsed = urlparse(self.config.storage_endpoint)
        #storage = ServerStorage(self.config, parsed)

class SQLiteStorageTestCase(TestCase):
    def setUp(self):
        self.db_path = "{}/pyprol_tests_sqlite_storage.db".format(os.environ["HOME"])

        self.config = Configuration()
        self.config.storage_endpoint = urlparse(
                "sqlite://{}".format(self.db_path))

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_url_expansion(self):
        self.config.storage_endpoint = "sqlite://$HOME/pyprol_sqlite_test.db"

        expanded_url = sqlite_storage.SQLiteStorage.var_expand(
                self.config.storage_endpoint)

        self.assertEqual(
                expanded_url,
                "sqlite://{}/pyprol_sqlite_test.db".format(os.environ["HOME"]))

    def test_sqlite(self):
        storage = sqlite_storage.SQLiteStorage(self.config)

    def test_wrong_path(self):
        self.config.storage_endpoint = urlparse(
                "sqlite:///a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/wrong_path")

        with self.assertRaises(RuntimeError):
            storage = sqlite_storage.SQLiteStorage(self.config)

    def test_save_timing(self):
        class Measure:
            name = "run_test"
            timestamp = date.today()
            timing = None

        measure = Measure()
        measure.timings = TimingStat(5, 0.100, 0.50, ['print', '+'])

        storage = sqlite_storage.SQLiteStorage(self.config)
        storage.save(measure)
        del(storage)

        conn = sqlite3.connect(self.config.storage_endpoint)
        cur = conn.cursor()
        cur.execute("SELECT * FROM timings")
        self.assertEqual(cur.rowcount, 1)

class StorageFactoryTestCase(TestCase):
    def setUp(self):
        self.config = Configuration({})
