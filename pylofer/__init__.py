from pylofer import Configuration
from pylofer.measurement import Measurement

from paste.registry import StackedObjectProxy


__all__ = ['Injector']

pylofer_proxy = StackedObjectProxy(name="pylofer")

class Injector(object):
    def __init__(self, app, config):
        self.config = Configuration(config)

        for injection in self.config.injections:
            injection_module = __import__(injection)
            injection_module.inject(config)
            self.injections.append(injection_module)

        if self.config.storage == "server":
            pylofer.client = MeasureClient(self.config.endpoint)

    def __call__(self, environ, start_response):
        if environ.has_key('paste.registry'):
            environ['paste.registry'].register(pylofer_proxy, Measurement())
        return self.app(environ, start_response)
