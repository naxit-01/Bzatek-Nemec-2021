import tornado.web
from tornroutes import route, prototype_route
from database import database
from admin import *
from moduls import *




g_port = 9999
db_path='BN_v.0.2/ROOT_server/database/database1.db'
paths=database.just_load_all(db_path)


def current_user():
	#pokud uzivatel nebyl authorizovan presmeruje na auth serrve, pokud prilozil cookies, cookies bude overeno a ziskano id user
    return True


prototype_route('/prototype', 'generic.html')
prototype1_route('/prototype1', 'generic.html', db_path, type='basic')
admin_route('/admin', 'mainpage.html', db_path, type='basic')

@route('/')
class SomeHandler(tornado.web.RequestHandler):
	def get(self):	

		print("root get")
		''' redirect to keycloak'''
		self.write(self.request.cookies)
		self.write("This part has not been programmed yet.")

'''@route('/admin')
class SomeHandler1(tornado.web.RequestHandler):
	def get(self):	
		print("admin get")
		admin.admin(db_path,self,type='basic')
		

	async def post(self):
		print("admin post")
		if self.get_argument("edit_btn", None) != None:
			self.write("This part has not been programmed yet.")
		print("ad")'''

@route(r'/(?P<parameterized>\w+)')
class SomeParameterizedRequestHandler(tornado.web.RequestHandler):
    def get(self, parameterized):
					print(parameterized)
					
        #goto = self.reverse_url(parameterized)
        #self.redirect(goto)

'''
@route('/(.*)')
class FetchStudent(tornado.web.RequestHandler):
	async def get(self,uri):
		print("multi get")
		if not current_user():
			self.redirect('/')
		parsed=uri.split("/")
		print(parsed)

		#NEFUNGUJE admin meni uri na "favicon.ico" todo: zjistit proc a jak se toho zbavit
		
		if(parsed[0]!=paths[0][0]):
			
			aport=database.find_ID_in_database(db_path,parsed[0],0)
					

			self.write(parsed[0]  + " This part has not been programmed yet.")
			self.write("We want to send you data from"+paths[aport][2])
		
	def post(self):
		print("multi Post")
		self.write("This part has not been programmed yet.")
		if self.get_argument("edit_btn", None) != None:
			self.write("This part has not been programmed yet.")
'''


application = tornado.web.Application(route.get_routes(), {'some app': 'settings'})

if __name__ == "__main__":
	application.listen(g_port)
	print("Client_sample running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
	