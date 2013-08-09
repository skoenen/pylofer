import json


__all__ = ['ConsoleStorage']

SCHEME = ('cons', 'console', 'stdout')

class ConsoleStorage(object):
    def __init__(self, config, parsed):
        self.config = config

    def save(measure):
        try:
            print(json.dump(measure))
        except TypeError:
            from logging import getLogger
            getLogger(__name__).error(
                    "Measure could not be converted:\n{}".format(measure))

