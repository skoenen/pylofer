from utils.introspection import respond_to


def as_bool(obj):
    if respond_to(obj, 'lower'):
        obj = obj.lower()

    return obj in ['yes', 'true']

