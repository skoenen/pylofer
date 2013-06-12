
class Configuration(dict):
    def __init__(self, config={}):
        self.config = config

    def should_measure(key):
        return self.config.fetch("measure.{}".format(key), False)
