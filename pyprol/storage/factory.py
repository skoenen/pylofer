try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from storage import server_storage, sqlite_storage, console_storage


__all__ = ["storage_factory"]

storage = None
SCHEME = ()

storage_impls = (sqlite_storage, server_storage, console_storage)

def storage_factory(config):
    if storage is None:
        parsed = urlparse(getattr(config, "storage_endpoint"))
        for storage_impl in storage_impls:
            for scheme in storage_impl.SCHEME:
                if parsed.scheme == scheme:
                    storage = storage_impl(config, parsed)

    return storage

