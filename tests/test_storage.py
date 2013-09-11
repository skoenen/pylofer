from unittest import TestCase
from tests import fixture

import json
import os
import sqlite3

from pyprol.storage import Storage
from pyprol.storage import sqlite_storage

#from pyprol.storage import server_storage
#from pyprol.storage import console_storage
#from pyprol.storage import file_storage

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class SQLiteStorageTestCase(TestCase):
    def assertMeasureAndResult(self, measure, result):
        db_repr = measure.to_db_repr()

        self.assertNotEqual(len(result), 0)
        self.assertEqual(len(result), len(db_repr))
        try:
            indexes = xrange(0, len(db_repr))
        except NameError:
            indexes = range(0, len(db_repr))

        for i in indexes:
            assert len(db_repr[i]) == len(result[i])
            assert db_repr[i] == result[i]

    def setUp(self):
        self.db_path = "{}/pyprol_tests_sqlite_storage".format(os.environ["HOME"])

        self.config = fixture.Configuration()
        self.config.storage_endpoint = urlparse(
                "sqlite://{}".format(self.db_path))

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_url_expansion(self):
        expanded_url = sqlite_storage.var_expand(
                "sqlite://$HOME/pyprol_sqlite_test.db")

        self.assertEqual(expanded_url,
                "sqlite://{}/pyprol_sqlite_test.db".format(os.environ["HOME"]))

        expanded_url = sqlite_storage.var_expand(
                "sqlite://$HOME/$USER/pyprol_sqlite_test.db")

        self.assertEqual(expanded_url,
                "sqlite://{}/{}/pyprol_sqlite_test.db".format(
                    os.environ["HOME"], os.environ["USER"]))

        expanded_url = sqlite_storage.var_expand(
                "sqlite://$HOME/$USER_pyprol/pyprol_sqlite_test.db")

        self.assertEqual(expanded_url,
                "sqlite://{}/{}_pyprol/pyprol_sqlite_test.db".format(
                    os.environ["HOME"], os.environ["USER"]))

    def test_sqlite(self):
        storage = sqlite_storage.SQLiteStorage(self.config)

    def test_wrong_path(self):
        self.config.storage_endpoint = urlparse(
                "sqlite:///a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/wrong_path")

        with self.assertRaises(RuntimeError):
            storage = sqlite_storage.SQLiteStorage(self.config)

    def test_save_timing(self):
        measure = fixture.Measure()

        storage = sqlite_storage.SQLiteStorage(self.config)
        storage.save(measure)
        del(storage)

        with sqlite3.connect(self.config.storage_endpoint.path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM timings;")
            result = cur.fetchall()

            self.assertMeasureAndResult(measure, result)

    def test_save_with(self):
        measure = fixture.Measure()

        with sqlite_storage.SQLiteStorage(self.config) as storage:
            storage.save(measure)

        with sqlite3.connect(self.config.storage_endpoint.path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM timings;")
            result = cur.fetchall()

            self.assertMeasureAndResult(measure, result)

class StorageFactoryTestCase(TestCase):
    def setUp(self):
        self.config = fixture.Configuration()

    def test_singleton(self):
        storage_test = Storage(self.config)
        self.assertEqual(storage_test, Storage())
        self.assertIsInstance(storage_test, sqlite_storage.SQLiteStorage)

