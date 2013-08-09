from measurement import measure


def inject(config):
    try:
        from pylons import WSGIController

        class WSGIController:
            _org_perform_call = _perform_call

            def _perform_call(self, func, args):
                __traceback_hide__ = 'before_and_this'
                result = _org_perform_call(func, args)
                measure(__name__)
                return result

    except ImportError:
        from logging import getLogger
        getLogger().info("No `pylons` in this context.")

