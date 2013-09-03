from unittest import TestCase
from tests import fixture
from pyprol import measurement


class MeasurementTestCase(TestCase):
    def setUp(self):
        self.config = fixture.Configuration()

    def test_init_shutdown(self):
        measurement.init(self.config)
        self.assertTrue(measurement.measurement._save_process.is_alive())
        self.assertIsNotNone(measurement.measurement._save_queue)

        measurement.shutdown()
        self.assertIsNone(measurement.measurement._save_process)
        self.assertIsNone(measurement.measurement._save_queue)

