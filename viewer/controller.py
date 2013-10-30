import os
import web


class NavElement:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class Controller:
    def __init__(self):
        self.settings_file = os.path.expanduser("~/pyprol_viewer_settings")

        self.settings_db = web.database(dbn="sqlite",
                db=os.path.expanduser("~/pyprol_viewer_settings"))

        self.settings_db.query(
                "CREATE TABLE IF NOT EXISTS sessions"
                " session_id VARCHAR(129) UNIQUE NOT NULL,"
                " atime DATETIME NOT NULL default datetime('now'),"
                " data TEXT")

        self.session_db = web.session.DBStore(self.settings_db, "sessions")

        self.nav_elements = [
                NavElement('Start', '/'),
                NavElement('Overview', '/overview'),
                NavElement('Measure', '/measure')]
        self.current = "Start"

        self.database = None
        self.render = web.template.render('templates/',
                base='layout',
                globals=globals())




class Viewer(Controller):
    def GET(self):
        global current

        current = "Start"
        return render.index(nav)

class Overview(Controller):
    def GET(self):
        global database
        global current

        current = "Overview"
        params = web.input(database=None, store=None)

        if store = None:


        if database is None:
            if params.database is None:
                redirect(nav_elements[0][0])

            database = web.database(dbn="sqlite", db=params.database)
        result = database.select('timings', offset=0, limit=30)
        measures = []
        for m in result:
            m['time_other'] = m['time_total'] - m['time_function']
            m['time_per_call'] = m['time_function'] - m['call_count']
            measures.append(m)

        return render.overview(measures)

class Measure:
    def GET(self, measure_id):
        global database
        global current

        current = "Measure"

        if database is None:
            return redirect(nav_elements[0][0])

        if measure_id < 0:
            return redirect(nav_elements[1][0])

        result = database.where("timings", measure_id=measure_id)

        measure = None
        for m in result:
            measure = MeasureModel(m)
            #measure.add_subcalls(
                    #database.where("timings_calls", measure_id=measure_id))

        print(measure)
        return render.measure(measure)

