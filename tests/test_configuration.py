from unittest import TestCase
from pyprol import configuration

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class ConfigurationTestCase(TestCase):
    def assertHasAttribute(self, obj, attr):
        self.assertTrue(hasattr(obj, attr))

    def setUp(self):
        self.polluted_config = {
                "pyprol.storage": "sqlite://$HOME/pyprol_test.db",
                "pyprol.instrumentations": "some.instrumentations.config, some.instrumentations.runner",
                "someother.option": "some value",
                "another.option": "with, a, list, value"}

        self.clean_config = {
                "pyprol.storage": "sqlite://$HOME/pyprol_test.db",
                "pyprol.instrumentations": "some.instrumentations.config, some.instrumentations.runner"}

        self.instrumentations = [
                "some.instrumentations.config",
                "some.instrumentations.runner",
                "pyprol.instrumentations.paste",
                "pyprol.instrumentations.pylons",
                "pyprol.instrumentations.sqlalchemy"]

        self.storage_endpoint = urlparse("sqlite://$HOME/pyprol_test.db")


    def test_config_filter(self):
        result = configuration.config_filter(self.polluted_config)

        self.assertEqual(result, self.clean_config)

    def test_instrumentation_list(self):
        result = configuration.instrumentation_list(
                self.clean_config["pyprol.instrumentations"])

        self.assertEqual(result,
                ["some.instrumentations.config",
                "some.instrumentations.runner"])

    def test_configuration(self):
        config = configuration.Configuration(self.polluted_config)

        self.assertEqual(
                config.instrumentations,
                self.instrumentations)

        self.assertEqual(
                config.storage_endpoint,
                self.storage_endpoint)

    def test_additional_keys(self):
        self.clean_config["pyprol.storage_server.storage_endpoint"] = "sqlite://$HOME/pyprol_server.db"
        self.clean_config["pyprol.measure.save_process_wait"] = 1

        config = configuration.Configuration(self.clean_config)

        self.assertHasAttribute(config, "storage_server")
        self.assertHasAttribute(config.storage_server, "storage_endpoint")
        self.assertHasAttribute(config, "measure")
        self.assertHasAttribute(config.measure, "save_process_wait")

