from pylofer import Configuration
from pylofer.measurement import MeasureClient


__all__ = ['Injector']

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
        return self.app(environ, start_response)
