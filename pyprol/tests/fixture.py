
class OptionContainer:
    def init(self, options):
        for key, value in options:
            setattr(self, key, value)
    pass

class Configuration:
    measure = None
    storage_endpoint = None

    def __init__(self):
        self.storage_endpoint = urlparse(
                "sqlite://$HOME/pyprol_tests_sqlite_storage")

        self.measure = OptionContainer({"save_process_wait": 0.01})

class StorageFactory:
    def __init__(self, config):
        pass

class Storage:
    pass


