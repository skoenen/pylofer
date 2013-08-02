from pyprol.utils import as_bool
from pyprol import instrumentations

def config_filter(item):
    return True if item.startswith("pyprol") else False

def instrumentation_map(item):
    if item is not None:
        item = item.strip()

    return item

class Configuration(object):
    def __init__(self, config={}):
        if config is not None:
            config = {}

        for c_key, c_value in filter(config_filter, config).items():
            key = c_key.split(".")[1].lower()

            if key == "instrumentations":
                self.instrumentations = map(instrumentation_map,
                        c_value.split(","))

            elif key == "storage":
                self.storage_endpoint = c_value
                self.storage = Storage(self)

            setattr(self, key, c_value)

        if as_bool(getattr(config, "pyprol.builtin_instrumentations", "True")):
            for instrumentation in instrumentations.__all__:
                self.instrumentations.append(instrumentation)
