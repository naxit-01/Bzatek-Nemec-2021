import tornado.ioloop
import tornado.web
from moduls import * # Contains a module for asynchronous requests
from tornroutes import route, prototype_route

g_port=9997

@route('/(.*)')
class mainPage(tornado.web.RequestHandler):
	async def get(self, uri):
		'''Return data to router'''
		parsed = uri.split("/")
		if self.request.arguments != None:
			print(self.request.arguments)
		self.write("Data about " + parsed[0] + " with ID: " + parsed[1])

application = tornado.web.Application([
    (r"/(.*)", mainPage)
])

if __name__ == "__main__":
	application.listen(g_port)
	print("API_tornado running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
