from pyprol import Configuration
from pyprol.measurement import Measurement

from paste.registry import StackedObjectProxy


__all__ = ['Injector']

pyprol_proxy = StackedObjectProxy(name="pyprol")

class Injector(object):
    def __init__(self, app, config):
        self.config = Configuration(config)

        for instrument in self.config.instruments:
            instrument_module = __import__(instrument)
            instrument_module.inject(config)
            self.instruments.append(instrument_module)

        if self.config.storage == "server":
            pyprol.client = MeasureClient(self.config.endpoint)

    def __call__(self, environ, start_response):
        if environ.has_key('paste.registry'):
            environ['paste.registry'].register(pyprol_proxy, Measurement())
        return self.app(environ, start_response)
