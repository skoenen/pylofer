from pyprol.measurement import measurement


def inject(config):
    try:
        from pylons import WSGIController

        class WSGIController:
            _org_perform_call = _perform_call

            def _perform_call(self, func, args):
                __traceback_hide__ = 'before_and_this'
                measure = measurement.enable(__name__)
                result = _org_perform_call(func, args)
                measurement.disable(measure)
                return result

    except ImportError:
        from logging import getLogger
        getLogger(__name__).info("No `pylons` in this context.")

