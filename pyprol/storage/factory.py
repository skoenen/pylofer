from . import server_storage, sqlite_storage, console_storage


__all__ = ["StorageFactory"]

_storage_impls = (sqlite_storage, server_storage, console_storage)
_storage = None
_config = None

def init(self, config):
    if _config is None:
        _config = config

    if _storage is None:
        parsed = getattr(_config, "storage_endpoint")

        for storage_impl in _storage_impls:
            for scheme in storage_impl.SCHEME:
                if parsed.scheme == scheme:
                    _storage = storage_impl(_config)

        return _storage

