from pyprol.storage import Storage

from multiprocessing import Process, Manager, Queue
from collections import namedtuple
from cProfile import Profile
from datetime import datetime
from logging import getLogger

import json
import time
import signal

try:
    from queue import Empty as QueueEmptyException
except ImportError:
    from Queue import Empty as QueueEmptyException


__all__ = ['Measure', 'TimingStat', 'enable', 'disable', 'init', 'shutdown']

log = getLogger(__name__)

_save_manager = None
_save_queue = None
_save_process = None

TimingStat = namedtuple(
        "TimingStat",
        ["timestamp", "name", "code", "call_count", "recursive_call_count",
        "time_total", "time_function", "calls"])

class Measure:
    def __init__(self,
            measure_point_name=None,
            save_queue=None,
            data=None):
        if data is None:
            self.point_name = measure_point_name
            self._save_queue = save_queue
            self._profile = Profile()
        else:
            self.point_name = data[0]
            self.load(data[1])

    def load(self, data):
        self.timings = data

    def start(self):
        self._profile.enable()
        return self

    def stop(self):
        self._profile.disable()
        self.stats = self._profile.getstats()
        self.timings = list()

        for stat in self.stats:
            if stat.calls is not None:
                calls = list()
                for call in stat.calls:
                    calls.append(TimingStat(datetime.utcnow(), self.point_name,
                            str(call.code), call.callcount, call.reccallcount,
                            call.totaltime, call.inlinetime, None))
            else:
                calls = None

            self.timings.append(
                    TimingStat(
                            datetime.utcnow(), self.point_name, str(stat.code),
                            stat.callcount, stat.reccallcount, stat.totaltime,
                            stat.inlinetime, calls))

        return self

    def save(self):
        self._save_queue.put_nowait((self.point_name, self.timings))
        return self

    def __str__(self):
        buf = "<{0}: point_name='{1}'".format(
                self.__class__, self.point_name)
        if hasattr(self, "stat"):
            buf += ", stat='{}'".format(self.stats)
        if hasattr(self, "timing"):
            buf += ", timing='{}'".format(self.timings)
        buf += ">"
        return buf

def enable(measure_point_name):
    global _save_queue
    return Measure(measure_point_name, _save_queue).start()

def disable(measure):
    return measure.stop().save()

class SaveProcess(Process):
    def __init__(self, config, save_queue, storage=None, *args, **kwargs):
        self._save_queue = save_queue
        self._config = config
        if storage is None:
            self.storage = Storage
        else:
            self.storage = storage
        super(SaveProcess, self).__init__(*args, **kwargs)

    def handle_term(self, signal, stack):
        self.shutdown = True
        self.timeout = 0.001

    def run(self):
        self.shutdown = False
        self.timeout = self._config.measure.save_process_wait

        # Define handler for the `terminate` signal and assign it.
        signal.signal(signal.SIGTERM, self.handle_term)

        # Wait `pyprol.measure.save_process_wait` time for a save request from
        # the measured process.
        # The timeout is needed, that this can react on the terminate signal.
        with self.storage(self._config) as storage:
            while True:
                try:
                    measure = Measure(
                            data=self._save_queue.get(timeout=self.timeout))
                    storage.save(measure)
                except QueueEmptyException:
                    log.debug("Reached timeout with empty queue.")

                if self.shutdown and self._save_queue.empty():
                    break


def init(config, storage=None):
    global _save_manager
    global _save_queue
    global _save_process

    if _save_manager is None:
        _save_manager = Manager()

    if _save_queue is None:
        _save_queue = _save_manager.Queue()

    if _save_process is None:
        if storage is None:
            _save_process = SaveProcess(config, _save_queue)
        else:
            _save_process = SaveProcess(config, _save_queue, storage)

        _save_process.start()

def shutdown():
    global _save_queue
    global _save_process

    while True:
        if not _save_process.is_alive():
            break
        elif _save_queue.empty():
            if _save_process.is_alive():
                _save_process.terminate()
                _save_process.join()

    _save_process = None
    _save_queue = None

