from pyprol.measurement import measurement

import importlib


def inject(config):
    try:
        paste_httpserver = importlib.import_module('paste.httpserver')

        _org_wsgi_start_respone = paste_httpserver.WSGIHandlerMixin.wsgi_start_response

        def wsgi_start_response(self, status, response_headers, exc_info=None):
            measure = measurement.enable(__name__)
            result = _org_wsgi_start_respone(self, status, response_headers, exc_info)
            measurement.disable(measure)
            return result

        paste_httpserver.WSGIHandlerMixin.wsgi_start_response = wsgi_start_response

    except ImportError:
        from logging import getLogger
        getLogger('pyprol.instrumentations.paste').info("No `paste` in current context.")

