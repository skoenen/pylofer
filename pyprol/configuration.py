from .utils import as_bool

from . import instrumentations as builtin_instrumentations

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


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

class OptionContainer(object):
    pass

class Configuration(object):
    instrumentations = None
    storage_endpoint = None

    def __init__(self, config=None):
        if config is not None:
            self.config = config_filter(config)

            for c_key, c_value in self.config.items():
                parts = c_key.split(".")
                self.set_option(parts[1:], c_value)

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

        if not hasattr(self, 'measure'):
            setattr(self, 'measure', OptionContainer())

        if not hasattr(self.measure, 'save_process_wait'):
            setattr(self.measure, 'save_process_wait', 0.01)

    def set_option(self, key_parts, value, base=None):
        if isinstance(key_parts, (list,)) and len(key_parts) > 1:
            self.set_option(key_parts[0], OptionContainer())
            self.set_option(key_parts[1], value, getattr(self, key_parts[0]))
        else:
            if base is None:
                base = self

            if isinstance(key_parts, (list,)):
                key = key_parts[0]
            else:
                key = key_parts

            if key == "instrumentations":
                setattr(base, 'instrumentations', instrumentation_list(value))

            elif key == "storage":
                value = urlparse(value)
                setattr(base, 'storage_endpoint', value)

            else:
                setattr(base, key, value)

