import tornado.web
from tornroutes import route
from database import database
from admin import *
from moduls import *

g_port = 9999
db_path='BN_v.0.2/ROOT_server/database/database1.db'
#db_path='database/database1.db'

paths=database.readTableRows(db_path, "paths")

admin_route('/admin', 'mainpage2.html', db_path)



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

def binaryToString(binaryDict):
	stringDict = {}
	for key, value in binaryDict.items():
		stringDict[key] = str(value)
	return stringDict


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

		if self.request.arguments != None:
			print("pred sendem")
			data = binaryToString(self.request.arguments) #dict value byla binarne a nesla poslat jako param
			response = await get_request_with_params(createUrl(index) + paths[index][0] + "/" + parsed[1], data)
		else:
			print("here")
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
			
			#if parsed[1] == None, pouzit id v cookie
			#Databaze je v upravach, pozdeji odkomentovat
			#response = await get_request(createUrl(index) + paths[index][0] + "/" + parsed[1])
			
			if parsed[0] == "student":
				ui_student = "http://127.0.0.1:9998/student/"
				response = await get_request(ui_student + parsed[1])
				self.write(response)
			elif parsed[0] == "rozvrh":
				ui_rozvrh = "http://127.0.0.1:9998/rozvrh/"
				response = await get_request(ui_rozvrh + parsed[1])
				self.write(response)
			elif parsed[0] == "ucitel": # Stejne nefunguje, nema jeho adresu v databazi a v api neni osetreno
				ui_ucitel = "http://127.0.0.1:9998/ucitel/"
				response = await get_request(ui_ucitel + parsed[1])
				self.write(response)
			else:
				print("Only student and teacher work, only improvised.")


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
	
