import tornado.ioloop
import tornado.web

g_port=9996
g_router="http://127.0.0.1:9999" # Mel by mit v databazi pro registrovaneho clienta

def binaryToString(binaryDict):
	stringDict = {}
	for key, value in binaryDict.items():
		stringDict[key] = str(value)
	return stringDict

class mainPage(tornado.web.RequestHandler):
	def get(self, uri):
            if(uri!='current_user'):
	            self.render("templates/loginPage.html")
				
	def post(self, uri):
		#Setting up cookie
		if not self.get_secure_cookie("mycookie"):
			self.set_secure_cookie("mycookie", "UserName",expires_days=1, domain='127.0.0.1')
			self.set_secure_cookie("UserID", self.get_argument("id")) 
			self.set_secure_cookie("UserType", self.get_argument("type"))             

			print("Your cookie was not set yet! Did it now.")
		else:
			print("Your cookie was set!")
		self.redirect(g_router + "/" + uri)
class currentUser(tornado.web.RequestHandler):
    def get(self):
        #if self.get_secure_cookie("UserID")!=None:
        '''user={
    		'mycookie':self.get_secure_cookie("mycookie").decode("utf-8"),
	    	'id':self.get_secure_cookie("UserID").decode("utf-8"),
		    'type':self.get_secure_cookie("UserType").decode("utf-8")
    	}'''
        user={
    		'mycookie':'admin',
	    	'id':'15',
		    'type':'admin'
    	}
        self.write(user)
        #else: self.write(None)
	    

application = tornado.web.Application([
    (r"/current_user", currentUser),
    (r"/(.*)", mainPage),
    
],cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")

if __name__ == "__main__":
	application.listen(g_port)
	print("Keycloak running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()
