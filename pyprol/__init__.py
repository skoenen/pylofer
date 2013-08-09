from pyprol import Configuration
from pyprol.measurement import measure
from pyprol.storage import storage_factory


__all__ = ['Pyprol']

class Pyprol(object):
    def __init__(self, app, config=None):
        self.config = Configuration(config)

        self.storage = storage_factory(self.config)

        for instrument in self.config.instruments:
            instrument_module = __import__(instrument)
            instrument_module.inject(config)
            self.instruments.append(instrument_module)

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
