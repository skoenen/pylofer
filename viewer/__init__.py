import codecs
import os
import sys
import web

from collections import namedtuple
from os import path
from web.webapi import header, NotFound as not_found

# For develop
sys.path.insert(0, path.dirname(path.abspath(__file__)))

from static import CssFiles, FontFiles, ImgFiles, JsFiles
from database import Database


NavEl = namedtuple("NavigationElement", ["url", "active", "name"])

urls = (
    '/', 'Viewer',
    '/overview', 'Overview',
    '/measure/(.*)', 'Measure',
    '/css/(.*)', 'CssFiles',
    '/js/(.*)', 'JsFiles',
    '/img/(.*)', 'ImgFiles',
    '/font/(.*)', 'FontFiles'
    )

nav_elements = [
    ('/', 'Start'),
    ('/overview', 'Overview'),
    ('/measure', 'Measure')]
current = "Start"

def nav():
    ret = []
    for n in nav_elements:
        if current == n[1]:
            ret.append(NavEl(n[0], 'active', n[1]))
        else:
            ret.append(NavEl(n[0], '', n[1]))
    return ret

database = None
render = web.template.render('templates/', base='layout', globals=globals())

class Viewer:
    def GET(self):
        return render.index(nav)

class Overview:
    global database
    global current

    def GET(self):
        current = "Overview"
        params = web.input(database=None)
        if database is None:
            if params.database is None:
                web.Redirect(nav_elements[0][0])

            database = Database(params.database)
        return render.overview(database.all())

class Measure:
    global database
    global current

    def GET(self, id):
        current = "Measure"
        params = web.input(id=-1)

        if database is None:
            web.Redirect(nav_elements[0][0])

        if params.id < 0:
            web.Redirect(nav_elements[1][0])

        measure = database.measure(params.id)
        render.measure(measure)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
