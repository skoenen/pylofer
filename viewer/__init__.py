import codecs
import multiprocessing
import os
import sys
import tempfile
import web

from collections import namedtuple
from os import path
from web.webapi import header, NotFound as not_found, Found as redirect

# For develop
sys.path.insert(0, path.dirname(path.abspath(__file__)))

from measurement import Measure as MeasureModel
from static import CssFiles, FontFiles, ImgFiles, JsFiles


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


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
