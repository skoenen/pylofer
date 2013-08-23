from pyprol.measurement import measurement


def inject(config):
    try:
        from paste import WSGIHandlerMixin

        class WSGIHandlerMixin:
            _org_wsgi_start_respone = wsgi_start_response

            def wsgi_start_response(self, status, response_headers, exc_info=None):
                measure = measurement.enable(__name__)
                result = _org_wsgi_start_respone(status, response_headers, exc_info)
                measurement.disable(measure)
                return result

    except ImportError:
        from logging import getLogger
        getLogger('pyprol.instrumentations.paste').info("No `paste` in current context.")

