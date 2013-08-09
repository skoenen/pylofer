from utils import as_bool
import instrumentations as builtin_instrumentations


__all__ = ["Configuration", "config_filter", "instrumentation_list"]

def config_filter(config):
    pyprol_config = {}
    for key, value in config.items():
        if key.startswith("pyprol"):
            key = key.lower()
            pyprol_config[key] = value
    return pyprol_config

def instrumentation_list(option):
    instr = []
    for item in option.split(","):
        instr.append(item.strip())
    return instr

class Configuration(object):
    instrumentations = None
    storage_endpoint = None

    def __init__(self, config={}):
        if config is not None:
            self.config = config_filter(config)

            for c_key, c_value in self.config.items():
                parts = c_key.split(".")
                set_option(parts[1:], c_value)

        else:
            self.config = {}

        if self.storage_endpoint is None:
            self.storage_endpoint = "sqlite://$HOME/pyprol.db"

        if as_bool(getattr(config, "pyprol.builtin_instrumentations", "True")):
            if self.instrumentations is None:
                self.instrumentations = []

            for instrument in dir(builtin_instrumentations):
                if not instrument.startswith("_"):
                    self.instrumentations.append(
                            "instrumentations.{0}".format(instrument))

    def set_option(self, key_parts, value, base=None):
        if isinstance(key_parts, (list,)):
            set_option(key_parts[0], object())
            set_option(key_parts[1], value, getattr(self, key_parts[0]))

        if base is None:
            base = self

        if key == "instrumentations":
            setattr(base, 'instrumentations', instrumentation_list(c_value))

        elif key == "storage":
            setattr(base, 'storage_endpoint', value)

        else:
            setattr(base, key_parts, value)

