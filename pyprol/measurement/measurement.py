from storage.factory import StorageFactory
from multiprocessing import Process, Queue
from collections import namedtuple

import yappi
import signal


_save_queue = None
_save_process = None

MeasurePointStat = namedtuple(
        "MeasurePointStat",
        ["call_count", "time_total", "time_in_function", "time_average"])

if not yappi.is_running():
    yappi.start()

def measure(measure_point_name):
    stats = yappi.get_func_stats(yappi.SORTTYPE_NAME)
    for func_stat in stats.func_stats:
        if func_stat.name == measure_point_name:
            _save_queue.put_nowait(MeasurePointStat(
                    func_stat.ncall, func_stat.ttot,
                    func_stat.tsub, func_stat.tavg))
            break

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
