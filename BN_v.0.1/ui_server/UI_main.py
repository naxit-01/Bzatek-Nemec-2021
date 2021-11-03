import tornado.web

g_port=9998

class mainPage(tornado.web.RequestHandler):
    def get(self):
        self.write("predstavte si rozvrh")

application = tornado.web.Application([
    (r"/", mainPage)
])

if __name__ == "__main__":
	application.listen(g_port)
	print("UI_sample running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()