from logging import getLogger
from pyprol.measurement import measurement

import importlib


log = getLogger('pyprol.instrumentations.pylons')

def inject(config):
    try:
        pylons_controllers = importlib.import_module('pylons.controllers')
        wsgi_controller = pylons_controllers.WSGIController
        wsgi_controller_perform_call = wsgi_controller._perform_call

        def _perform_call(self, func, args):
            __traceback_hide__ = 'before_and_this'
            measure = measurement.enable(
                    "pylons.controllers.core.WSGIController._perform_call")
            result = wsgi_controller_perform_call(self, func, args)
            measurement.disable(measure)
            return result

        wsgi_controller._perform_call = _perform_call
        log.info("injected into pylons.controllers.WSGIController._perform_call")

    except ImportError as e:
        log.info("No `pylons` in this context. {}".format(e))
        log.debug(e)

