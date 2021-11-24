from .database import *
from .tornroutes import route
import tornado.ioloop
import tornado.web



def TmpltDtbs(dbHndlr,tableNames):
            dtbs=[]
            for i,tableName in enumerate(tableNames):
                table={
                    "tableName":tableName,
                    "tableRows":'',
                    "tableColumns":'', 
                    "editID":[],
                    "PK":dbHndlr.findPK(tableName)
                    }
                dtbs.append(table)

            return dtbs

def showPage(self, dbHndlr):
    for i, table in enumerate(self._dtbs):
        table["tableRows"]=dbHndlr.readTableRows(table["tableName"])
        table["tableColumns"]=dbHndlr.readTableColumns(table["tableName"])

    self.render(self._template, database=self._dtbs)

def admin_route(uri, template, dbHndlr):
    @route(uri, name=uri)
    class admin_handler(tornado.web.RequestHandler):
        
        _dbHndlr=dbHndlr
        _dtbs=TmpltDtbs(_dbHndlr,_dbHndlr.readTableNames())
        _template = template

        def get(self):

            showPage(self, self._dbHndlr)
        
        def post(self):
            for i,table in enumerate(self._dtbs):
                table["PK"]=self._dbHndlr.findPK(table["tableName"])
                for row in self._dbHndlr.readTableRows(table["tableName"]):

                    if(self.get_argument(str("Edit_button"+table["tableName"]+row[table["PK"]]), None) != None):
                        table["editID"].append(row[table["PK"]])

                        showPage(self, self._dbHndlr)
            
                    if(self.get_argument(str("Save_button"+table["tableName"]+row[table["PK"]]), None) != None):
                        task=[]                    
                        for i in range(len(table["tableColumns"])):
                            task.append(self.get_argument(str("input"+table["tableName"]+row[table["PK"]]+str(i))))
                        task.append(str(row[table["PK"]]))
                        self._dbHndlr.updateTableRow(table["tableName"], task)
                        table["editID"].remove(row[table["PK"]])

                        showPage(self, self._dbHndlr)
                
                    if(self.get_argument(str("Delete_button"+table["tableName"]+row[table["PK"]]), None) != None):                       
                        self._dbHndlr.deleteTableRow(table["tableName"], row[table["PK"]])
                        try: table["editID"].remove(row[table["PK"]])
                        except: print("nebylo v editID")

                        showPage(self, self._dbHndlr)

                if self.get_argument(str("Add_button"+table["tableName"]), None) != None:
                    self._dbHndlr.addTableRow(table["tableName"])

                    showPage(self, self._dbHndlr)
			    
    return admin_handler

