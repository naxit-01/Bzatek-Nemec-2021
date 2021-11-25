import tornado.ioloop
import tornado.web

g_port=9996
g_router="http://127.0.0.1:9999" # Mel by mit v databazi pro registrovaneho clienta

class route(object):

    _routes = []

    def __init__(self, uri, name=None, kwargs={}):
        print("__init__")
        self._uri = uri
        self.name = name
        self.kwargs = kwargs

    def __call__(self, _handler):
        print("__call__")
        """gets called when we class decorate"""
        name = self.name or _handler.__name__
        self._routes.append(tornado.web.url(self._uri, _handler, self.kwargs, name=name))
        return _handler

    @classmethod
    def get_routes(cls):
        print("get_routes")
        return cls._routes


@route('/(.*)')
class mainPage(tornado.web.RequestHandler):
	def get(self, uri):
		self.render("templates/loginPage.html")

	def post(self, uri):
		#Setting up cookie
		if not self.get_cookie("mycookie"):
			self.set_cookie("mycookie", "UserName") # Neni secure, jen testovaci
			self.set_cookie("UserID", self.get_argument("id")) # Neni secure, jen testovaci
			self.set_cookie("UserType", self.get_argument("type")) # Neni secure, jen testovaci
			print("Your cookie was not set yet! Did it now.")
		else:
			print("Your cookie was set!")
		self.redirect(g_router + "/" + uri)

application = tornado.web.Application([
    (r"/(.*)", mainPage)
])

if __name__ == "__main__":
	application.listen(g_port)
	print("Keycloak running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
