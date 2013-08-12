from os import path

import json


__all__ = ['FileStorage']

SCHEME = ("file")

class FileStorage(object):
    """ Saves measure data in files.
        Expects an path where to store the files.
        So an url for this storage is made from the following components:

        URL:
            SCHEME      PATH                    OPTIONS
            file://     $HOME/pyprol/database   ?...

        OPTIONS:
            KEY         DIVIDER     VALUE
            [a-z\-]+    =           [a-z\-0-9A-Z]

        KEY:
            Key           | Valueformat       | Description
            --------------+-------------------+-------------------------------
            max-size      | \d+[KMGT]         | Maximum size of a single file.
            format        | (csv|json)        | Format to save the values in.
    """
    def __init__(self, config):
        self.path = self.config.storage_endpoint.path

        if "?" in self.path:
            param_str = self.path.split("?")
            for param in param_str.split("&"):
                if "=" in param:
                    key, value = param.split("=")
                    setattr(self, key, value)

                else:
                    setattr(self, param, True)

    def _convert(self, measure):
        if self.format == "json":
            try:
                return json.dumps(measure)
            except TypeError:
                from logging import getLogger
                getLogger(__name__).error(
                        "Measure could not be converted '{}'".format(measure))
        elif self.format == "csv":
            csv_format_string = ''
            element_count = len(measure)



    def save(self, measure):
        f = file_for(measure)
        f.write(_convert(measure))
        f.flush()

