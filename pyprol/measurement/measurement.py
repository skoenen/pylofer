import yappi


__all__ = ['Measurement']

MeasurePointStat = namedtuple(
        "MeasurePointStat",
        ['call_count', 'time_total', 'time_in_function', 'time_average'])

class Measurement(object):
    def __init__(self, config):
        self.config = config
        if not yappi.is_running():
            yappi.start()

    def measure(self, measure_point_name):
        stats = yappi.get_func_stats(yappi.SORTTYPE_NAME)
        measure_point_stat = None
        for func_stat in stats.func_stats:
            if func_stat.name == measure_point_name:
                measure_point_stat = MeasurePointStat(
                        func_stat.ncall, func_stat.ttot,
                        func_stat.tsub, func_stat.tavg)

                break

        return Measure(self.config,
                measure_point_name,
                measure_point_stat).save()

    def start_new(self, measure_point_name):
        return Measure(self.config, measure_point_name).start()

class Measure(object):
    def __init__(self,
            config,
            measure_point_name,
            measure_point_stat=None,
            data=None):

        self.config = config
        self.storage = self.config.storage
        self.aspects = self.config.aspects

        if data:
            self.name = data["name"]
            self.data = data["measures"]

        else:
            self.name = measure_point_name
            self.data = [measure_point_stat]

    def start(self):
        for aspect in self.aspects:
            aspect.start()
        return self

    def end(self):
        for aspect in self.aspects:
            self.data.append({aspect.name: aspect.end()})

        self.save()
        return self

    def save(self):
        self.storage.save(self)

        return self

