
import web
import backend

urls = (
    '/', 'index',
    '/upload','upload',
)
app = web.application(urls,globals())
render = web.template.render('templates')

class index():
    def GET(self):
        return render.index(data=backend.get_data())
class upload():
    def POST(self):
        (err,msg) = backend.insert_data(web.data())
        if err == 0:
            return web.ok
        else:
            return web.internalerror(msg)

if __name__ == "__main__":
    app.run()
