import tornado.ioloop
import tornado.web
from moduls import * # Contains a module for asynchronous requests
from tornroutes import route, prototype_route

g_port=9998
g_router="http://127.0.0.1:9999"

@route('/(.*)')
class mainPage(tornado.web.RequestHandler):
	async def get(self, uri):
		'''Ask router for api data'''

		parsed = uri.split("/")
		if parsed[0] == "rozvrh":
			data = {
				'datum':"1.1.2022",
				'type':"prednasky"
			}
			response = await get_request_with_params(g_router + "/api/" + uri, data)
			self.write("Data o uzivateli: " + response)
		else:
			response = await get_request(g_router + "/api/" + uri)
			self.write("Data o uzivateli: " + response)

application = tornado.web.Application([
    (r"/(.*)", mainPage)
])

if __name__ == "__main__":
	application.listen(g_port)
	print("UI_tornado running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
