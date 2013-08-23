from . import server_storage, sqlite_storage, console_storage


__all__ = ["StorageFactory"]

class StorageFactory(object):
    _instance = None
    _storage_impls = (sqlite_storage, server_storage, console_storage)

    def __new__(cls, config):
        if cls._instance is None:
            try:
                cls._instance = cls.__init__(cls, config)
            except TypeError:
                cls._instance = super(StorageFactory, cls).__new__(cls, config)

        print(cls._instance)
        return cls._instance

    def __init__(self, config):
        self._storage = None
        self.config = config

    def storage(self):
        if self._storage is None:
            parsed = getattr(self.config, "storage_endpoint")
            for storage_impl in self._storage_impls:
                for scheme in storage_impl.SCHEME:
                    if parsed.scheme == scheme:
                        self._storage = storage_impl(self.config)

        return self._storage

