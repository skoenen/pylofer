from unittest import TestCase

import measurement
import yappi


class MeasurementTestCase(TestCase):
    def setUp(self):
        pass

    def test_yappi_start(self):
        self.assertTrue(yappi.is_running())

    def test_measure(self):
        pass
