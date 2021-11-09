from database import database
from tornroutes import route
import tornado.ioloop
import tornado.web

def TmpltDtbs(db_path,tableNames):
            dtbs=[]
            for i,tableName in enumerate(tableNames):
                table={
                    "tableName":tableName,
                    "tableRows":'',
                    "tableColumns":'', 
                    "editID":[],
                    "PK":database.findPK(db_path,tableName)
                    }
                dtbs.append(table)

            return dtbs

def showPage(self):
    for i, table in enumerate(self._dtbs):
        table["tableRows"]=database.readTableRows(self._db_path,table["tableName"])
        table["tableColumns"]=database.readTableColumns(self._db_path,table["tableName"])

    self.render(self._template, database=self._dtbs)

def admin_route(uri, template, db_path):
    @route(uri, name=uri)
    class admin_handler(tornado.web.RequestHandler):
        
        _dtbs=TmpltDtbs(db_path,database.readTableNames(db_path))
        _template = template
        _db_path = db_path

        def get(self):
            showPage(self)
        
        def post(self):
            for i,table in enumerate(self._dtbs):
                table["PK"]=database.findPK(self._db_path,table["tableName"])
                for row in database.readTableRows(self._db_path,table["tableName"]):

                    if(self.get_argument(str("Edit_button"+table["tableName"]+row[table["PK"]]), None) != None):
                        table["editID"].append(row[table["PK"]])

                        showPage(self)
            
                    if(self.get_argument(str("Save_button"+table["tableName"]+row[table["PK"]]), None) != None):
                        task=[]                    
                        for i in range(len(table["tableColumns"])):
                            task.append(self.get_argument(str("input"+table["tableName"]+row[table["PK"]]+str(i))))
                        task.append(str(row[table["PK"]]))
                        database.updateTableRow(self._db_path,table["tableName"], task)
                        table["editID"].remove(row[table["PK"]])

                        showPage(self)
                
                    if(self.get_argument(str("Delete_button"+table["tableName"]+row[table["PK"]]), None) != None):                       
                        database.deleteTableRow(self._db_path, table["tableName"], row[table["PK"]])
                        try: table["editID"].remove(row[table["PK"]])
                        except: print("nebylo v editID")

                        showPage(self)

                if self.get_argument(str("Add_button"+table["tableName"]), None) != None:
                    database.addTableRow(self._db_path,table["tableName"])

                    showPage(self)
			    
    return admin_handler

