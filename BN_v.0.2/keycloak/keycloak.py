import tornado.ioloop
import tornado.web
from tornroutes import route, prototype_route

g_port=9996
g_router="http://127.0.0.1:9999" # Mel by mit v databazi pro registrovaneho clienta

@route('/(.*)')
class mainPage(tornado.web.RequestHandler):
	def get(self, uri):
		self.render("templates/loginPage.html")

	def post(self, uri):
		#Vystavit cookie
		self.redirect(g_router + "/" + uri)

application = tornado.web.Application([
    (r"/(.*)", mainPage)
])

if __name__ == "__main__":
	application.listen(g_port)
	print("Keycloak running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()