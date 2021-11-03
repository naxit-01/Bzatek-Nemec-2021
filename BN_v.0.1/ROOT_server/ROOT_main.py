import tornado.web
from tornroutes import route
import database
from admin import admin

g_port = 9999
paths=database.connect_database('ROOT_server/database1.db')


def current_user():
	#pokud uzivatel nebyl authorizovan presmeruje na auth serrve, pokud prilozil cookies, cookies bude overeno a ziskano id user
    return True

def findID(list,arg,position):
	for i,record in enumerate(list):
		if arg==list[i][position]:
			return  i
	print("Error-findID didnt find anything")
	return "Error"

@route('/')
class SomeHandler(tornado.web.RequestHandler):
	def get(self):	
					''' redirect to keycloak'''
					self.write(self.request.cookies)
					self.write("This part has not been programmed yet.")



@route('/(.*)')
class FetchStudent(tornado.web.RequestHandler):
	def get(self,uri):
					if not current_user():
						self.redirect('/')

					parsed=uri.split("/")

					if(parsed[0]==paths[0][0]):
						admin.admin(paths,self)
						

					aport=findID(paths,parsed[0],0)
					

					self.write(parsed[0]  + " This part has not been programmed yet.")
					self.write("We want to send you data from"+paths[aport][2])
								


application = tornado.web.Application(route.get_routes(), {'some app': 'settings'})

if __name__ == "__main__":
	application.listen(g_port)
	print("Client_sample running on port: " + str(g_port) + "...")
	tornado.ioloop.IOLoop.instance().start()