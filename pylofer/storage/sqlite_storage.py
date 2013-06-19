from storage import Storage

import sqlite3

_SQL_STORAGE = None
_SQLITE_TYPE_MAP = {
                    "list":    "TABLE",
                    "dict":    "TABLE",
                    "int":     "INTEGER",
                    "float":   "DECIMAL",
                    "string":  "VARCHAR",
                    "unicode": "VARCHAR"
                    }

class SQLiteContainer(object):
    def __init__(self, measurement, config={}):
        self.typ = measurement.typ
        self.structures = []
        _structure_for(measurement.data)

    def _structure_for(self, data):
        assert isinstance(data, (list))
        structure = []
        for obj in data:
            assert isinstance(obj, (dict))
            for key in obj.keys():
                if isinstance(obj[key], (list)):
                    structures.append(_structure_for(obj[key]))
                elif key not in structure:
                    structure[key] = _SQLITE_TYPE_MAP[type(obj[key])]

    def check():
        pass

class SQLiteStorage(Storage):
    def __new__(self, **args):
        if not _SQL_STORAGE:
            _SQL_STORAGE = super(SQLiteStorage, self).__new__(**args)
        return _SQL_STORAGE

    def __init__(self, config={}):
        self.config = config
        self.container = {}

    def save(self, measurement):
        container = get_container_for(measurement)
        container.check()
        container.append(measurement)
        self.con.container
