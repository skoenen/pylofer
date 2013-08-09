__all__ = ['respond_to']

def respond_to(obj, method_name):
    try:
        return callable(getattr(obj, method_name))
    except AttributeError:
        return False

