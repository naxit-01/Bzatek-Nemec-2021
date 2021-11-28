import os
from moduls import *
import json

g_port = 9999

dbHndlr=DBHandler(os.path.join(os.path.dirname(__file__), "static/database.db"))

def current_user(self):
	#Returns None if user isnt authenticated by a cookie
	user={
		'mycookie':self.get_cookie("mycookie"),
		'id':self.get_cookie("UserID"),
		'type':self.get_cookie("UserType")
	}
	return user

def createToken(self):
	if current_user(self)['type']=='admin': return "asdfadmin"
	if current_user(self)['type']=='teacher': return "asdfteacher"
	if current_user(self)['type']=='student': return "asdfstudent"

	#!!!! vyresit cookie u api
	return "asdfadmin"


admin_route('/admin', "adminpage.html", dbHndlr)

@route('/')
class RootHandler(tornado.web.RequestHandler):
	def get(self):
		'''
		Zjistit prihlaseni, pokud neni hodit na keycloak, pokud je nacist default stranku (plati jen pro root)
		'''
		if not current_user(self)['id']:
			authenticate(self,None, dbHndlr)
		else:
			print("Logged in as: " + self.get_cookie("UserID") + self.get_cookie("UserType"))
		
		self.redirect("http://127.0.0.1:9999/ui/student/"+str(current_user)(self)['id'])

@route('/api/(.*)')
class ApplicationProgrammingInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		'''
		Nema cookie, protoze neni user, ale ui server s jinou ip, autentizovat pres keycloak
		!!!! vyresit cookie
		if not current_user(self):
			authenticate(self,"api/" + uri)'''

		parsed = uri.split("/")
		index = dbHndlr.findIndex(parsed[0], "apis")
			
		if index==None:
			print("findIndex: Could not find page in database.")
			self.redirect("/404")
		
		params = (
    		('params', json.dumps({
					"token": createToken(self),
					"data": binaryToString(self.request.arguments) #dict value byla binarne a nesla poslat jako param
					})),
		)
		response = await get_request_with_params_and_headers(createUrl(dbHndlr.readTableRows("apis")[index]) + parsed[0] + '/' + parsed[1],{
    		'accept': 'application/json',
		},params)
		self.write(response)

@route('/ui/(.*)')
class UserInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		if not current_user(self)['id']:
			authenticate(self,"ui/" + uri, dbHndlr)
		else:
			parsed = uri.split("/")
			index = dbHndlr.findIndex(parsed[0], "uis")
			
			if index==None:
				print("findIndex: Could not find page in database.")
				self.redirect("/404")
			
			# pouzit id v cookie a smazat(prepsat) nasledujici
			if len(parsed) == 1:
				parsed.insert(1, "264")

			response = await get_request(createUrl(dbHndlr.readTableRows("uis")[index]) + parsed[0]  + '/' + parsed[1])
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
	
