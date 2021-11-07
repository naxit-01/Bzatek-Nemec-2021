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
	#pokud uzivatel nebyl authorizovan presmeruje na auth serrve, pokud prilozil cookies, cookies bude overeno a ziskano id user
	return self.get_cookie("mycookie")
    #return True


prototype_route('/prototype', 'generic.html')
prototype1_route('/prototype1', 'generic.html', db_path, type='basic')
admin_route('/admin', 'mainpage.html', db_path, type='basic')

@route('/')
class RootHandler(tornado.web.RequestHandler):
	def get(self):	
		#print("root get")
		#print(paths)
		'''
		Zjistit prihlaseni, pokud neni hodit na keycloak, pokud je nacist default stranku (plati jen pro root)
		Tuto cast vystipnout do funkce a pouzivat ve vsech routes, jen vzdy pokracovat na pozadovanou uri
		'''
		
		if current_user(self) == None:
			# 5 je keycloak, je TMP struktura databaze se bude menit
			self.redirect(paths[5][2] + ":" + str(paths[5][3]))
			return
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
class Test(tornado.web.RequestHandler):
	async def get(self,uri):
		# must be logged (cookie)
		parsed = uri.split("/")
		information_type_index = -1
		for i, path in enumerate(paths):
			if path[0] == parsed[0]: # V databazi neni student/teacher/predmet -> pokud bude 1 api server, neni potreba resit
				information_type_index = i
				break
		
		if information_type_index == -1:
			print("Error! Unknown request path")

		# 2 je umisteni destination_ip v databazi, 3 je port, mozna lepsi integrovat do sebe uvnitr databaze
		response = await get_request(paths[information_type_index][2] + ":" + str(paths[information_type_index][3]) + "/" + paths[information_type_index][0] + "/" + parsed[1])
		self.write(response)

@route('/ui/(.*)')
class FetchStudent(tornado.web.RequestHandler):
	async def get(self,uri):
		#print("multi get")
		'''
		if not current_user():
			self.redirect('/')
		'''
		parsed=uri.split("/")
		
		# Pouzit vyhledavani z api, udelat nezavislou funkci
		if parsed[0] == "student":
			#information_type_index = 4 Je potreba zmenit strukturu databaze na admin\ui\api a v pod tabulkach resit seznamy adres
			ui_student = "http://127.0.0.1:9998"
			# /student by slo pres paths[information_type_index][0], zase jako v hledani api
			response = await get_request(ui_student + "/student/" + parsed[1])
			self.write(response)
		else:
			print("Only student works.")

		#NEFUNGUJE admin meni uri na "favicon.ico" todo: zjistit proc a jak se toho zbavit
		'''
		if(parsed[0]!=paths[0][0]):
			
			aport=database.find_ID_in_database(db_path,parsed[0],0)
					

			#self.write(parsed[0]  + " This part has not been programmed yet.")
			self.write("We want to send you data from" + paths[aport][2])
		'''
	def post(self):
		print("multi Post")
		self.write("This part has not been programmed yet.")
		if self.get_argument("edit_btn", None) != None:
			self.write("This part has not been programmed yet.")

@route('/(.*)')
class PageNotFound(tornado.web.RequestHandler):
	def get(self,uri):
		parsed=uri.split("/")
		if parsed[0] != "" and parsed[0] != "admin" and parsed[0] != "api" and parsed[0] != "ui":
			self.render("templates/PageNotFound.html") # Doesnt render image, only text needs fixing

application = tornado.web.Application(route.get_routes(), {'some app': 'settings'})

if __name__ == "__main__":
	application.listen(g_port)
	print("Router_tornado running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
	
