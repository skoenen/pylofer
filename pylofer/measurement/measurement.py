
__all__ = ['Measurement']

class Measurement(object):
    def __init__(self, config, storage):
        self.config = config
        self.storage = storage

    def start_new(self, measure_point_name):
        measure = Measure(self.config,
                self.storage,
                measure_point_name,
                self.config.measure.aspects)
        return measure.start()

class Measure(object):
    def __init__(self,
            config,
            storage,
            measure_point_name,
            aspect_names={},
            data=None):

        self.config = config
        self.storage = storage

        if data:
            self.name = data["name"]
            self.data = [measure for measure in data["measures"]]

        else:
            self.name = measure_point_name
            self.data = []
            self.aspects = []
            for aspect_module, aspect_name in aspect_names.iteritems():
                aspect = __import__(aspect_module, aspect_name)
                self.aspects.append(aspect[aspect_name](self.config, self.name))

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

