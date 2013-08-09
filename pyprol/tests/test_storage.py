from unittest import TestCase
from os import environ

from configuration import Configuration
from storage import server_storage, sqlite_storage, console_storage, storage_factory

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


endpoint = "pyprol.storage_endpoint"

class ServerStorageTestCase(TestCase):

    def setUp(self):
        self.config = Configuration()

    def test_udp(self):
        self.config[endpoint] = "udp://127.0.0.1:65333"

        parsed = urlparse(self.config.storage_endpoint)
        storage = ServerStorage(self.config, parsed)

    def test_udp6(self):
        self.config[endpoint] = "udp6://[::1]:65333"

        parsed = urlparse(self.config.storage_endpoint)
        storage = ServerStorage(self.config, parsed)

    def test_unix(self):
        self.config[endpoint] = "unix:///var/run/pyprol.server.socket"

        parsed = urlparse(self.config.storage_endpoint)
        storage = ServerStorage(self.config, parsed)

class SqliteStorageTestCase(TestCase):
    def setUp(self):
        self.config = Configuration()

    def test_url_expansion(self):
        self.config.storage_endpoint = "sqlite://$HOME/pyprol_sqlite_test.db"

        expanded_url = sqlite_storage.var_expand(self.config.storage_endpoint)

        self.assertEqual(
                expanded_url,
                "sqlite://{}/pyprol_sqlite_test.db".format(environ["HOME"]))

    def test_sqlite(self):
        self.config[endpoint] = "sqlite://{}/pyprol_sqlite_test.db".format(environ["HOME"])

class StorageFactoryTestCase(TestCase):
    def setUp(self):
        self.config = Configuration({})
