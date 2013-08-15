from storage.factory import StorageFactory
from multiprocessing import Process, Queue
from collections import namedtuple
from cProfile import Profile

import signal


__all__ = ['Measure', 'enable', 'disable', 'init', 'shutdown']

_save_queue = None
_save_process = None

TimingStat = namedtuple(
        "TimingStat",
        ["call_count", "time_total", "time_in", "calls"])

class Measure:
    _save_queue = None

    point_name = None

    timings = None
    memory = None

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
        self.timings = TimingStat(
                stat.callcount, stat.totaltime, stat.inlinetime, stat.calls)
        return self

    def save(self):
        self._save_queue.put_nowait(self)
        return self

def enable(measure_point_name):
    return Measure(measure_point_name, _save_queue).start()

def disable(measure):
    return measure.stop().save()

def _convert_cprofile_calls(calls):
    for call in calls:
        pass

def _save_measurement(config, queue):
    shutdown = False
    storage = StorageFactory(config).storage()
    queue_timeout = config.measure.save_process_wait

    def handle_term():
        storage.close()
        shutdown = True
        queue_timeout = 0.001
    signal.signal(signal.SIGTERM, handle_term)

    while not shutdown:
        try:
            storage.save(queue.get(), queue_timeout)
        except Queue.Empty:
            pass


def init(storage):
    if _save_queue is None:
        _save_queue = Queue()

    if _save_process is None:
        _save_process = Process(target=_save_measurement,
                args=(storage, _save_queue))

        _save_process.start()

def shutdown():
    while not _save_queue.empty():
        time.sleep(0.01)

    _save_process.terminate()
    _save_process.join()
    _save_queue.close()
