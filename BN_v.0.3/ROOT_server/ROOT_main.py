import os
from moduls import *

g_port = 9999

dbHndlr=DBHandler(os.path.join(os.path.dirname(__file__), "static/database.db"))

paths=dbHndlr.readTableRows("paths")
uis=dbHndlr.readTableRows("uis")
apis=dbHndlr.readTableRows("apis")

'''
pomocne funkce zabalit do moduls, mozna pribalit i tabulky vyse
problemy: pomocne funkce potrebuji tabulky a je nutno je importovat za ne (sem), zaroven DBHandler je v modulu (potreba importovat pred nim)
mozna vytvorit hlavnni modul ktery importuje ostatni a vytvori tabulky, sem do main pote importovat jen ten hlavni?
'''

def current_user(self):
	#Returns None if user isnt authenticated by a cookie
	return self.get_cookie("mycookie")

def authenticate(self, uri):
	# 4 je keycloak, keycloak musi byt v paths nebo zmenit zde
	if uri == None:
		self.redirect(paths[4][2] + ":" + str(paths[4][3]))
	else:
		self.redirect(paths[4][2] + ":" + str(paths[4][3]) + "/" + uri)

def findIndex(self, keyword, table):
	try:
		for i, tableRow in enumerate(table):
			if tableRow[0] == keyword:
				return i
	except:
		print("findIndex: Could not find page in database.")
		self.redirect("/404")

def createUrl(index, table):
	# 2 je umisteni destination_ip v databazi, 3 je port
	return "http://" + table[index][2] + ":" + str(table[index][3]) + '/'

def binaryToString(binaryDict):
	stringDict = {}
	for key, value in binaryDict.items():
		stringDict[key] = str(value)
	return stringDict

admin_route('/admin', "adminpage.html", dbHndlr)

@route('/')
class RootHandler(tornado.web.RequestHandler):
	def get(self):
		'''
		Zjistit prihlaseni, pokud neni hodit na keycloak, pokud je nacist default stranku (plati jen pro root)
		'''
		if not current_user(self):
			authenticate(self,None)
		else:
			print("Logged in as: " + self.get_cookie("mycookie"))

		# default adresa, nikdo krome / tu uz nebude
			self.redirect("http://127.0.0.1:9999/ui/student/264")

@route('/api/(.*)')
class ApplicationProgrammingInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		'''
		Nema cookie, protoze neni user, ale ui server s jinou ip, autentizovat pres keycloak
		
		if not current_user(self):
			authenticate(self,"api/" + uri)'''

		parsed = uri.split("/")
		index = findIndex(self, parsed[0], apis)

		if self.request.arguments != None:
			data = binaryToString(self.request.arguments) #dict value byla binarne a nesla poslat jako param
			response = await get_request_with_params(createUrl(index, apis) + apis[index][0] + "/" + parsed[1], data)
		else:
			response = await get_request(createUrl(index, apis) + apis[index][0] + "/" + parsed[1])
		self.write(response)

@route('/ui/(.*)')
class UserInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		if not current_user(self):
			authenticate(self,"ui/" + uri)
		else:
			parsed = uri.split("/")
			index = findIndex(self, parsed[0], uis)
			
			# pouzit id v cookie a smazat(prepsat) nasledujici
			if len(parsed) == 1:
				parsed.insert(1, "264")

			response = await get_request(createUrl(index, uis) + uis[index][0] + "/" + parsed[1])
			self.write(response)

@route('/(.*)')
class PageNotFound(tornado.web.RequestHandler):
	def get(self,uri):
		parsed=uri.split("/")
		if parsed[0] != "" and parsed[0] != "admin" and parsed[0] != "api" and parsed[0] != "ui":
			self.render("PageNotFound.html")

application = tornado.web.Application(
	route.get_routes(),
	{'some app': 'settings'},
 	static_path=os.path.join(os.path.dirname(__file__), "static"), 
	template_path=os.path.join(os.path.dirname(__file__), "templates") 
	)

if __name__ == "__main__":
	application.listen(g_port)
	print("Router_tornado running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
	
