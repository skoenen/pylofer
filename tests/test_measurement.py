from unittest import TestCase
from tests import fixture
from datetime import datetime
from pyprol import measurement

import sys
import os

class TimingStatTestCase(TestCase):
    def test_timingstat(self):
        obj = measurement.TimingStat(
                datetime.utcnow(), "test", "test.code.py", 1, 0, 0.4, 0.2, None)

        assert hasattr(obj, 'timestamp')
        assert hasattr(obj, 'name')
        assert hasattr(obj, 'code')
        assert hasattr(obj, 'call_count')
        assert hasattr(obj, 'recursive_call_count')
        assert hasattr(obj, 'time_total')
        assert hasattr(obj, 'time_function')
        assert hasattr(obj, 'calls')

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
                indexes = xrange(0, len(a.calls))
            except NameError:
                # Use the xrange function, that is named range in python 3
                indexes = range(0, len(a.calls))

            for i in indexes:
                self.assertEqualTiming(a.calls[i], b.calls[i])

    def assertEqualMeasure(self, a, b):
        self.assertIsInstance(a, measurement.Measure)
        self.assertIsInstance(b, measurement.Measure)

        self.assertEqual(a.point_name, b.point_name)
        if hasattr(a, "timings") and hasattr(b, "timings"):
            self.assertEqual(len(a.timings), len(b.timings))

            try:
                indexes = xrange(0, len(a.timings))
            except NameError:
                indexes = range(0, len(a.timings))

            for i in indexes:
                self.assertEqualTiming(a.timings[i], b.timings[i])

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

        self.assertEqual(recv_measure.timings, send_measure.timings)
        self.assertEqual(recv_measure.point_name, send_measure.point_name)

    def test_enable_disable(self):
        storage = fixture.Storage(self.config)
        measurement.init(self.config, fixture.Storage)

        measure = measurement.enable("testing")
        fixture.nop()
        measurement.disable(measure)
        measurement.shutdown()

        self.assertEqualMeasure(fixture.Storage().last(), measure)

