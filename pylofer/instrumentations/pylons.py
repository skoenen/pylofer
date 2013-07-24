from pylofer.measurements import Measurement

from pylons import WSGIController

perform_call = WSGIController.__dict__["_perform_call"]

def _perform_call(self, func, args):
    measure = Measurement().start()
    __traceback_hide__ = 'before_and_this'
    result = perform_call(self, func, args)
    measure.end()
    return result

WSGIController.__dict__["_perform_call"] = _perform_call
