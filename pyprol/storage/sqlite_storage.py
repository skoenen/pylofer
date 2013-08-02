from sql_alchemy_storage import SQLAlchemyStorage

import sqlite3

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

class SQLiteStorage(SQLAlchemyStorage):
    def __init__(self, config={}):
        self.config = config
        self.container = {}

    def save(self, measurement):
        container = get_container_for(measurement)
        container.check()
        container.append(measurement)
        self.con.container
