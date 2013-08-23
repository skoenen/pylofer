from .configuration import Configuration
from .storage.factory import StorageFactory
from . import measurement


_pyprol = None

class Pyprol(object):
    def __init__(self, config=None):
        self.config = Configuration(config)

        self.storage = StorageFactory(self.config).storage()
        measurement.init(self.storage)

        for instrument in self.config.instruments:
            instrument_module = __import__(instrument)
            instrument_module.inject(config)
            self.instruments.append(instrument_module)

        measurement.init(self.config)

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

    def __del__(self):
        measurement.shutdown()

def inject(global_conf, **config):
    _pyprol = Pyprol(config)

