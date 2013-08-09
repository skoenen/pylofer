from measurement import measure


def inject(config):
    try:
        from paste import WSGIHandlerMixin

        class WSGIHandlerMixin:
            _org_wsgi_start_respone = wsgi_start_response

            def wsgi_start_response(self, status, response_headers, exc_info=None):
                result = _org_wsgi_start_respone(status, response_headers, exc_info)
                measure(__name__)
                return result

    except ImportError:
        from logging import getLogger
        getLogger('pyprol.instrumentations.paste').info("No `paste` in current context.")

