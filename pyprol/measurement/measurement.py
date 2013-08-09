from storage import storage_factory
from multiprocessing import Process, Queue

from collections import namedtuple

import yappi


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

def _save_measurement(storage, queue):
    while True:
        storage.save(queue.get())

_save_queue = Queue()
_save_process = Process(target=_save_measurement, args=(storage_factory(), _save_queue))

