import os
from moduls import *

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
			print("Logged in as: " + current_user(self)['UserType'] + " ID " + current_user(self)['UserID'])
		url=createUrl(dbHndlr.readTableRows("paths")[dbHndlr.findIndex("admin", "paths")]) + "ui/"+(current_user)(self)['UserType']+"/"+(current_user)(self)['UserID']
		self.redirect(url)

@route('/ui/(.*)')
class UserInterface(tornado.web.RequestHandler):
	async def get(self,uri):
		'''Comment here'''
		if not current_user(self)['UserID']:
			authenticate(self,"ui/" + uri, dbHndlr)
		else:

			parsed = uri.split("/")
			index = dbHndlr.findIndex(parsed[0], "uis")
			
			if index == None:
				print("findIndex: Could not find page in database.")
				self.redirect("/404")

			if len(parsed) == 1 or parsed[1] == '':
				parsed.insert(1, str(current_user(self)['UserID']))

			try:
				response = await get_request_with_cookies(createUrl(dbHndlr.readTableRows("uis")[index]) + parsed[0]  + '/' + parsed[1], self.cookies)
				self.write(response)
			except Exception as e:
				print("Router:UserIterface:GetRequest: error: " + str(e))
				self.write("Can not connect to external server.")

@route('/api/(.*)')
class ApplicationProgrammingInterface(tornado.web.RequestHandler):
	'''Comment here'''
	async def get(self,uri):
		if not current_user(self)['UserID']:
			authenticate(self,"api/" + uri, dbHndlr)
		else:

			parsed = uri.split("/")
			index = dbHndlr.findIndex(parsed[0], "apis")
			
			if index==None:
				print("findIndex: Could not find page in database.")
				self.redirect("/404")

			if len(parsed) == 1 or parsed[1] == '':
				parsed.insert(1, str(current_user(self)['UserID']))

			if self.request.arguments:
				params = {"params" : self.get_argument("params")} # Necessary to decode from binary form, can not just pass them raw
			else:
				params = {}

			cookies = {"UserType": current_user(self)['UserType'], "UserID": current_user(self)['UserID']} #For sending unsecure cookies, dont know how to decode them in fastapi
			try:
				response = await get_request_with_params_and_cookies(createUrl(dbHndlr.readTableRows("apis")[index])+"api/" + parsed[0] + '/' + parsed[1], params, cookies) #Secure with self.cookies
				self.write(response)
			except Exception as e:
				print("Router:ApplicationProgrammingInterface:GetRequest: error: " + str(e))
				self.write("Can not connect to external server.")

@route('/(.*)')
class PageNotFound(tornado.web.RequestHandler):
	def get(self,uri):
		#parsed=uri.split("/")
		#if parsed[0] != "" and parsed[0] != "admin" and parsed[0] != "api" and parsed[0] != "ui":
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
	
