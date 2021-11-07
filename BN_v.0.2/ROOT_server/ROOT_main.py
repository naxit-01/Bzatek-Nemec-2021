import tornado.web
from tornroutes import route, prototype_route
from database import database
from admin import *
from moduls import *

g_port = 9999
#db_path='BN_v.0.2/ROOT_server/database/database1.db'
db_path='database/database1.db'
paths=database.just_load_all(db_path)

def current_user(self):
	#Returns None if user isnt authenticated by a cookie
	return self.get_cookie("mycookie")

def authenticate(self, uri):
	# 5 je keycloak, je TMP struktura databaze se bude menit
	self.redirect(paths[5][2] + ":" + str(paths[5][3]) + "/" + uri)

def findIndex(self, keyword):
	for i, path in enumerate(paths):
		if path[0] == keyword:
			return i
	self.redirect("/404")

def createUrl(index):
	# Pokud se zmeni databaze nutno zmenit druhy argument
	# 2 je umisteni destination_ip v databazi, 3 je port
	return "http://" + paths[index][2] + ":" + str(paths[index][3]) + '/'
	

prototype_route('/prototype', 'generic.html')
prototype1_route('/prototype1', 'generic.html', db_path, type='basic')
admin_route('/admin', 'mainpage.html', db_path, type='basic')

@route('/')
class RootHandler(tornado.web.RequestHandler):
	def get(self):
		'''
		Zjistit prihlaseni, pokud neni hodit na keycloak, pokud je nacist default stranku (plati jen pro root)
		Tuto cast vystipnout do funkce a pouzivat ve vsech routes, jen vzdy pokracovat na pozadovanou uri
		'''
		if not current_user(self):
			authenticate(self,None)
		else:
			print("Logged in as: " + self.get_cookie("mycookie"))
		# mit vlastni adresu v databazi, divne ne?, ale sel bych do toho
		# zde by byla default adresa, nikdo krome / tu uz nebude
			self.redirect("http://127.0.0.1:9999/ui/student/264")
		
		#self.write(self.request.cookies)
		#self.write("This part has not been programmed yet.")

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

'''
@route(r'/(?P<parameterized>\w+)')
class SomeParameterizedRequestHandler(tornado.web.RequestHandler):
    def get(self, parameterized):
					print(parameterized)
					
        #goto = self.reverse_url(parameterized)
        #self.redirect(goto)
'''
@route('/api/(.*)')
class ApplicationProgrammingInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		'''
		Nema cookie, protoze neni user, ale ui server s jinou ip
		print(self.request.remote_ip) Nevraci port, jen ip. Pro localhost nepouzitelne
		'''
		'''if not current_user(self):
			authenticate(self,"api/" + uri)'''
		parsed = uri.split("/")
		index = findIndex(self, parsed[0])

		response = await get_request(createUrl(index) + paths[index][0] + "/" + parsed[1])
		self.write(response)

@route('/ui/(.*)')
class UserInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		if not current_user(self):
			authenticate(self,"ui/" + uri)
		else:
			parsed = uri.split("/")
			index = findIndex(self, parsed[0])
			
			#Databaze je v upravach, pozdeji odkomentovat
			#response = await get_request(createUrl(index) + paths[index][0] + "/" + parsed[1])
			
			if parsed[0] == "student":
				ui_student = "http://127.0.0.1:9998/student/"
				response = await get_request(ui_student + parsed[1])
				self.write(response)
			elif parsed[0] == "ucitel": # Stejne nefunguje, nema jeho adresu v databazi a v api neni osetreno
				ui_ucitel = "http://127.0.0.1:9998/ucitel/"
				response = await get_request(ui_ucitel + parsed[1])
				self.write(response)
			else:
				print("Only student and teacher work, only improvised.")

		# Vojtuv bordel
		#NEFUNGUJE admin meni uri na "favicon.ico" todo: zjistit proc a jak se toho zbavit
		'''
		if(parsed[0]!=paths[0][0]):
			
			aport=database.find_ID_in_database(db_path,parsed[0],0)
					

			#self.write(parsed[0]  + " This part has not been programmed yet.")
			self.write("We want to send you data from" + paths[aport][2])
		
	def post(self):
		print("multi Post")
		self.write("This part has not been programmed yet.")
		if self.get_argument("edit_btn", None) != None:
			self.write("This part has not been programmed yet.")'''

@route('/(.*)')
class PageNotFound(tornado.web.RequestHandler):
	def get(self,uri):
		parsed=uri.split("/")
		if parsed[0] != "" and parsed[0] != "admin" and parsed[0] != "api" and parsed[0] != "ui":
			self.render("templates/PageNotFound.html") # Doesnt render image, only text, needs fixing

application = tornado.web.Application(route.get_routes(), {'some app': 'settings'})

if __name__ == "__main__":
	application.listen(g_port)
	print("Router_tornado running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
	
