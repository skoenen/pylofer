from pyprol.measurement import Measurement

def inject(config):
    try:
        from paste import WSGIHandlerMixin

        class WSGIHandlerMixin:
            _org_wsgi_start_respone = wsgi_start_response

            def wsgi_start_response(self, status, response_headers, exc_info=None):
                measure = Measurement(config).start_new()
                result = _org_wsgi_start_respone(status, response_headers, exc_info)
                measure.end()
                return result

    except ImportError:
        from pyprol.utils import logger
        logger.get_logger().info("No `paste` in current context.")

