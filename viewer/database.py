import sqlite3

from measurement import Measure

class Database(object):
    _db = None

    def __new__(cls, path=None):
        if cls._db is None:
            if path is None:
                raise RuntimeError("No database path.")
            cls._db = SQLiteDatabase(path)

        return cls._db

    def __getattr__(self, name):
        return getattr(self.__dict__['_db'], name)

    def __setattr__(self, name, val):
        return setattr(self.__dict__['_db'], name, val)

class SQLiteDatabase:
    measure_select = ("SELECT"
              " t.measure_id,"
              " t.timestamp,"
              " t.measure_session,"
              " t.measure_point,"
              " t.code,"
              " t.call_count,"
              " t.recursive_call_count,"
              " t.time_total,"
              " t.time_function,"
              " (t.time_function / t.call_count) as time_per_call,"
              " (t.time_total - t.time_function) as time_other "
              "FROM timings as t")

    submeasure_select = ("SELECT"
              " tc.measure_id,"
              " tc.timestamp,"
              " tc.measure_point,"
              " tc.code,"
              " tc.call_count,"
              " tc.recursive_call_count,"
              " tc.time_total,"
              " tc.time_function,"
              " (tc.time_function / tc.call_count) as time_per_call,"
              " (tc.time_total - tc.time_function) as time_other "
              "FROM timings_calls as tc")

    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.con.row_factory = sqlite3.Row

    def all(self):
        result = self.con.execute(self.measure_select)
        return result.fetchall()

    def range(self, start=None, amount=None):
        cursor = self.con.cursor()
        if start is None:
            self.start = 0 + self.start
        else:
            self.start = start

        if amount is None:
            self.amount = 50
        else:
            self.amount = amount

        result = cursor.execute(self.measure_select +
                " LIMIT " + str(self.amount) +
                " OFFSET " + str(self.start))
        return result.fetchall()

    def measure(self, id):
        result = self.con.execute(self.measure_select +
                "WHERE t.measure_id = ?", id)
        measure = Measure(result.fetchone())

        result = self.con.execute(self.submeasure_select +
                "WHERE tc.id = ?", measure.id)
        measure.add_subcalls(result.fetchall())

        return measure
