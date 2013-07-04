try:
    from cProfile import Profile, Stats
except ImportError:
    from cProfile import cProfile, Stats

__all__ = ["MeasureAspect", "TimingAspect", "MemoryAspect", "CallAspect"]

class MeasureAspect(object):
    def __init__(self, config, name):
        self.config = config
        self.name = name
        self.typ = "GENERIC"

    def end(self):
        return self._data

class TimingAspect(MeasureAspect):
    def __init__(self, config, name):
        super(TimingMeasurement, self).__init__(config, name)
        self.typ = "TIMING"
        self.profile = Profile()

    def start(self):
        self.profile.enable()

    def end(self):
        self._data = Stats(self.profile).total_tt
        return {self.typ: self._data}

class MemoryAspect(MeasureAspect):
    def __init__(self, config, name):
        super(TimingMeasurement, self).__init__(config, name)
        self.typ = "MEMORY"

class CallAspect(MeasureAspect):
    def __init__(self, config, name):
        super(TimingMeasurement, self).__init__(config, name)
        self.typ = "CALL"
        self.profile = Profile()

    def start(self):
        self.profile.enable()

    def end(self):
        self._data = Stats(self.profile).total_call
        return {self.typ: self._data}

