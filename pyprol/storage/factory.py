try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from storage import server_storage, sqlite_storage, console_storage


__all__ = ["StorageFactory"]

class StorageFactory(object):
    _storage = None
    _storage_impls = (sqlite_storage, server_storage, console_storage)

    def __init__(self, config):
        self.config = config

    def storage(self):
        if _storage is None:
            parsed = urlparse(getattr(config, "storage_endpoint"))
            for storage_impl in _storage_impls:
                for scheme in storage_impl.SCHEME:
                    if parsed.scheme == scheme:
                        _storage = storage_impl(config, parsed)

        return storage

