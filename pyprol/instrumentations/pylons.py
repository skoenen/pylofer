from pyprol.measurement import Measurement

try:
    from pylons import WSGIController

    class WSGIController:
        _org_perform_call = _perform_call

        def _perform_call(self, func, args):
            measure = Measurement().start()
            __traceback_hide__ = 'before_and_this'
            result = _org_perform_call(func, args)
            measure.end()
            return result

except ImportError:
    from pyprol.utils import logger
    logger.get_logger().info("No `pylons` in this context.")

