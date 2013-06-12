from pylons import WSGIController

perform_call = WSGIController.__dict__["_perform_call"]

def _perform_call(self, func, args):
    pass
