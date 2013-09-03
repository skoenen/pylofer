from .configuration import Configuration
from .storage import Storage
from . import measurement

import importlib


__all__ = ['Pyprol', 'inject']
_pyprol = None

class Pyprol(object):
    def __init__(self, app, config):
        self.app = app
        self.config = Configuration(config)

        self.instrumentations = []
        for instrument in self.config.instrumentations:
            instrument_module = importlib.import_module(instrument)
            instrument_module.inject(self.config)
            self.instrumentations.append(instrument_module)

        measurement.init(self.config)

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

def inject(global_conf, **config):
    def pyprol_filter(app):
        return Pyprol(app, config)

    return pyprol_filter

