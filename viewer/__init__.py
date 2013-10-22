import web


urls = (
    '/', 'Viewer'
    )

render = web.template.render('templates/')

class Viewer:
    def GET(self):
        return render.index()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
