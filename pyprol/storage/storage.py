from pyprol.storage import sqlite_storage, server_storage, console_storage

class Storage(object):
    _storage_impls = (sqlite_storage, server_storage, console_storage)
    _storage = None

    def __new__(cls, config=None):
        if cls._storage is None:
            if config is None:
                raise RuntimeError(
                        "Could not initialize storage, no configuration.")

            endpoint = getattr(config, "storage_endpoint")

            for storage_impl in cls._storage_impls:
                for scheme in storage_impl.SCHEME:
                    if endpoint.scheme == scheme:
                        cls._storage = storage_impl.IMPL(config)

        return cls._storage

    def __getattr__(self, name):
        return getattr(self.__dict__['_storage'], name)

    def __setattr__(self, name, val):
        return setattr(self.__dict__['_storage'], name, val)

