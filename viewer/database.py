import sqlite3

class Database:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.con.row_factory = sqlite3.Row

    def all(self):
        result = self.con.execute(
                "SELECT"
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
                "from timings as t")
        return result.fetchall()

    def measure(self, id):
        result = self.con.execute(
                "SELECT"
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
                "from timings as t"
                "where t.measure_id = ?", id)

        return result.fetchone()
