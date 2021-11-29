import os
from moduls import *
import json

g_port = 9999

dbHndlr=DBHandler(os.path.join(os.path.dirname(__file__), "static/database.db"))

def current_user(self):
	#Returns None if user isnt authenticated by a cookie
	try: user={
		'mycookie':self.get_secure_cookie("mycookie").decode('utf8'), 
		'UserID':self.get_secure_cookie("UserID").decode('utf8'),
		'UserType':self.get_secure_cookie("UserType").decode("utf-8")
	}
	except: user={
		'mycookie':self.get_secure_cookie("mycookie"), 
		'UserID':self.get_secure_cookie("UserID"),
		'UserType':self.get_secure_cookie("UserType")
	}
	return user

def createToken(self):
	if current_user(self)['UserType']=='admin': return "asdfadmin"
	if current_user(self)['UserType']=='teacher': return "asdfteacher"
	if current_user(self)['UserType']=='student': return "asdfstudent"
	return "asdfadmin"


admin_route('/admin', "adminpage.html", dbHndlr)

@route('/')
class RootHandler(tornado.web.RequestHandler):
	def get(self):
		'''
		Zjistit prihlaseni, pokud neni hodit na keycloak, pokud je nacist default stranku (plati jen pro root)
		'''
		if not current_user(self)['UserID']:
			authenticate(self,None, dbHndlr)
		else:
			print("Logged in as: " + current_user(self)['UserID'] + current_user(self)['UserType'])
		url="http://127.0.0.1:9999/ui/student/"+str((current_user)(self)['id'])
		print(url)
		self.redirect(url)

@route('/api/(.*)')
class ApplicationProgrammingInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		if not current_user(self)['UserID']:
			""" predelat request"""
			user = json.loads(await get_request('http://127.0.0.1:9996/current_user'))
			self.set_secure_cookie("mycookie",user["mycookie"])
			self.set_secure_cookie("UserID",user["id"])
			self.set_secure_cookie("UserType2",user["type"])
		
		
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
		if not current_user(self)['UserID']:
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
	template_path=os.path.join(os.path.dirname(__file__), "templates"),
	cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__" 
	)

if __name__ == "__main__":
	application.listen(g_port)
	print("Router_tornado running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
	
