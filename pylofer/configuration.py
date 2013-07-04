
def config_filter(item):
    return True if item.startswith("pylofer") else False

def measure_filter(item):
    return True if item.startswith("pylofer.measure") else False

class Configuration(object):
    def __init__(self, config={}):
        for k in filter(config_filter, config):
            key = k.split(".")[1].lower()

            if key == "injections":
                self.injections = [v.strip() for v in config[k].split(",")]
            elif key == "measure":
                self.measure = object()

                for m in filter(measure_filter, config):
                    mpoint = m.split(".")[2].lower().strip()
                    setattr(self.measure, mpoint, True)

            setattr(self, key, config[k])

        self.builtin_injections = getattr(self,
                "bultin_injections", "pylofer.injections").lower()

        if self.builtin_injections != "none":
            pass

    def should_measure(key):
        return self.config.fetch("measure.{}".format(key), False)
