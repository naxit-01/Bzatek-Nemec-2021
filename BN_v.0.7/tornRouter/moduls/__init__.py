from .request_async import *
from .admin import *
from .tornroutes import *
from .database import *

def authenticate(self, uri, dbHndlr):
	authID=dbHndlr.findIndex("keycloak", "paths")
	if uri == None:
		self.redirect("http://" +dbHndlr.readTableRows("paths")[authID][2] + ":" + str(dbHndlr.readTableRows("paths")[authID][3]))
	else:
		self.redirect("http://" +dbHndlr.readTableRows("paths")[authID][2] + ":" + str(dbHndlr.readTableRows("paths")[authID][3]) + "/" + uri)

def binaryToString(binaryDict):
	stringDict = {}
	for key, value in binaryDict.items():
		stringDict[key] = str(value)
	return stringDict

def createUrl(data):
	# 2 je umisteni destination_ip v databazi, 3 je port
	return "http://" + data[2] + ":" + str(data[3]) + '/' 