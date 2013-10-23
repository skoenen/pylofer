import codecs
import os

from web.webapi import header

class StaticFiles:
    def filename(self, name):
        path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                self.type, name)
        return path

    def filesize(self, name):
        return os.stat(self.filename(name)).st_size

    def GET(self, name):
        ret = u''
        with codecs.open(self.filename(name), 'r', encoding='utf-8') as f:
            ret += f.read()

        header(u'Content-Type', self.content_type)
        header(u'Content-Length', self.filesize(name))
        return ret

class CssFiles(StaticFiles):
    def __init__(self):
        self.type = u'css'
        self.content_type = u'text/css; charset=utf-8'

class FontFiles(StaticFiles):
    def __init__(self):
        self.type = u'fonts'

    def GET(self, name):
        ext = os.path.splitext(name)[1][1:]

        if ext == 'woff':
            self.content_type = u'application/font-woff'
        elif ext == 'ttf':
            self.content_type = u'application/octet-stream'
        elif ext == 'otf':
            self.content_type = u'application/octet-stream'
        elif ext == 'eot':
            self.content_type = u'application/octet-stream'
        elif ext == 'svg':
            self.content_type = u'application/octet-stream'
        else:
            not_found("Unknown font type.")

        ret = None
        with open(self.filename(name), 'r') as f:
            ret = f.read()

        header(u'Content-Type', self.content_type)
        header(u'Content-Length', self.filesize(name))
        return ret

class ImgFiles(StaticFiles):
    def __init__(self):
        self.type = u'js'
        self.content_type = u'text/javascript; charset=utf-8'

class JsFiles(StaticFiles):
    def __init__(self):
        self.type = u'js'
        self.content_type = u'application/x-javascript; charset=utf-8'

