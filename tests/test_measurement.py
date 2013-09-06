from unittest import TestCase
from tests import fixture
from pyprol import measurement

import sys


class MeasurementTestCase(TestCase):
    def assertEqualTiming(self, a, b):
        self.assertEqual(a.code, b.code)
        self.assertEqual(a.call_count, b.call_count)
        self.assertEqual(a.recursive_call_count, b.recursive_call_count)
        self.assertEqual(a.time_total, b.time_total)
        self.assertEqual(a.time_function, b.time_function)
        self.assertEqual(a.calls, b.calls)

        if a.calls is not None and b.calls is not None:
            try:
                # Check if we should use the python 2 xrange function
                indexes = xrange(0,len(a.calls))
            except NameError:
                # Use the xrange function, that is named range in python 3
                indexes = range(0, len(a.calls))

            for i in indexes:
                self.assertEqualTiming(a.calls[i], b.calls[i])

    def assertEqualMeasure(self, a, b):
        self.assertIsInstance(a, measurement.Measure)
        self.assertIsInstance(b, measurement.Measure)

        self.assertEqual(a.point_name, b.point_name)
        if hasattr(a, "timing") and hasattr(b, "timing"):
            self.assertEqualTiming(a.timing, b.timing)

        elif hasattr(a, "timing"):
            assert False

        elif hasattr(b, "timing"):
            assert False

    def setUp(self):
        self.config = fixture.Configuration()

    def test_init_shutdown(self):
        measurement.init(self.config)
        self.assertTrue(measurement.measurement._save_process.is_alive())
        self.assertIsNotNone(measurement.measurement._save_queue)

        measurement.shutdown()
        self.assertIsNone(measurement.measurement._save_process)
        self.assertIsNone(measurement.measurement._save_queue)

    def test_save_load(self):
        queue = fixture.Queue()
        send_measure = measurement.Measure("testing", queue)
        send_measure.start().stop().save()

        recv_measure = measurement.Measure(data=queue.get())

        self.assertEqual(recv_measure.timing, send_measure.timing)
        self.assertEqual(recv_measure.point_name, send_measure.point_name)

    def test_enable_disable(self):
        storage = fixture.Storage(self.config)
        measurement.init(self.config, fixture.Storage)

        measure = measurement.enable("testing")
        fixture.nop()
        measurement.disable(measure)
        measurement.shutdown()

        self.assertEqualMeasure(fixture.Storage().last(), measure)
        self.assertIn("nop", fixture.Storage().last().timing.code)

