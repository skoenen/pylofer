from logging import getLogger
from pyprol.measurement import measurement

import importlib


log = getLogger('pyprol.instrumentations.paste')

def inject(config):
    try:
        paste_httpserver = importlib.import_module('paste.httpserver')

        _org_wsgi_start_respone = paste_httpserver.WSGIHandlerMixin.wsgi_start_response

        def wsgi_start_response(self, status, response_headers, exc_info=None):
            measure = measurement.enable(
                    "paste.httpserver.WSGIHandlerMixin.wsgi_start_response")
            result = _org_wsgi_start_respone(self, status, response_headers,
                    exc_info)
            measurement.disable(measure)
            return result

        paste_httpserver.WSGIHandlerMixin.wsgi_start_response = wsgi_start_response

    except ImportError:
        log.info("No `paste` in current context.")

