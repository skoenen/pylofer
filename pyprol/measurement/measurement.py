from pyprol.storage import Storage

from multiprocessing import Process, Queue
from collections import namedtuple
from cProfile import Profile

import time
import signal


__all__ = ['Measure', 'enable', 'disable', 'init', 'shutdown']

_save_queue = None
_save_process = None

TimingStat = namedtuple(
        "TimingStat",
        ["code",
        "call_count",
        "recursive_call_count",
        "time_total",
        "time_function",
        "calls"])

class Measure:
    def __init__(self, measure_point_name, save_queue):
        self.point_name = measure_point_name
        self._save_queue = save_queue
        self._profile = Profile()

    def start(self):
        self._profile.enable()
        return self

    def stop(self):
        self._profile.disable()
        stat = self._profile.getstats()[0]

        return self

    def save(self):
        self._save_queue.put_nowait(self)
        return self

    def transform(self):
        calls = []
        for call in self.stat.calls:
            calls.append(TimingStat(call.code, call.callcount,
                    call.reccallcount, call.totaltime, call.inlinetime, None))

        self.timing = TimingStat(
                self.stat.callcount, self.stat.reccallcount,
                self.stat.totaltime, self.stat.inlinetime, calls)

def enable(measure_point_name):
    global _save_queue
    return Measure(measure_point_name, _save_queue).start()

def disable(measure):
    return measure.stop().save()

class SaveProcess(Process):
    def __init__(self, config, save_queue, *args, **kwargs):
        self._save_queue = save_queue
        self._config = config
        super(SaveProcess, self).__init__(*args, **kwargs)

    def run(self):
        shutdown = False
        timeout = self._config.measure.save_process_wait

        # Define handler for the `terminate` signal and assign it.
        def handle_term():
            shutdown = True
            timeout = 0.001
        signal.signal(signal.SIGTERM, handle_term)

        # Wait `pyprol.measure.save_process_wait` time for a save request from
        # the measured process.
        # The timeout is needed, that this can react on the terminate signal.
        with Storage(self._config) as storage:
            print(self._save_queue)
            while not shutdown and not self._save_queue.empty():
                try:
                    measure = self._save_queue.get(timeout)
                    measure.transform()
                    storage.save(measure)
                except Queue.Empty:
                    pass


def init(config):
    global _save_queue
    global _save_process

    if _save_queue is None:
        _save_queue = Queue()

    if _save_process is None:
        _save_process = SaveProcess(config, _save_queue)
        _save_process.start()

def shutdown():
    global _save_queue
    global _save_process

    _save_process.terminate()
    _save_process.join()
    _save_queue.close()

    _save_process = None
    _save_queue = None

