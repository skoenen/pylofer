try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from pyprol import storage as storages
from pyprol.configuration import ConfigurationError


_STORAGE = None

SCHEME = []

class Container(object):
    def __init__(self, namespace=None, config=None):
        if config is None:
            self.config = {}
        else:
            self.config = config

        if namespace is None:
            self.namespace = ""
        else:
            self.namespace = namespace

    def save(self, obj):
        raise NotImplementedError("Do not know how to save.")

class Storage(object):
    def __new__(self, **args):
        if not _STORAGE:
            _STORAGE = super(self.__class__, self).__init__(**args)
        return _STORAGE

    def __init__(self, config):
        raise NotImplementedError("Abstract class")

    def save(self, obj):
        raise NotImplementedError("Abstract class")

    def _get_container(self, obj):
        container = self.container.get(obj.typ, None)
        if container is None:
            container = self.container_class(obj.typ, self.config)
            self.container[obj.typ] = container

        return container

def storage_factory(config):
    if hasattr(config, "storage_endpoint"):
        parsed = urlparse(getattr(config, "storage_endpoint"))

        for storage_impl in storages:
            for scheme in storage_impl.SCHEME:
                if parsed.scheme == scheme:
                    return storage_impl(config, describe_str)

    else:
        raise ConfigurationError("No endpoint to store measures.")

