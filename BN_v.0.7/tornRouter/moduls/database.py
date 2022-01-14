import sqlite3
from sqlite3.dbapi2 import Error
# Create a SQL connection to our SQLite database 

class DBHandler():
    _db_path = ""

    def __init__(self,path):
        self._db_path = path

    def connect_database(self):  
        return sqlite3.connect(self._db_path) 

    def close_connection(self, con):
        con.close()

    def readTableNames(self):
        con=self.connect_database()
        res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablenames = []
        for name in res.fetchall():
            tablenames.append(name[0])
        self.close_connection(con)
        return tablenames

    def readTableRows(self, tablename):
        con=self.connect_database()
        cur=con.cursor()
        query = "SELECT * FROM "+tablename
        cur.execute(query)
        tasks = cur.fetchall()
        self.close_connection(con)
        return tasks

    def readTableColumns(self, tablename):
        con=self.connect_database()
        cur=con.cursor()
        res=cur.execute("SELECT * FROM "+tablename).description
        columns =[]
        for name in res:
            columns.append(name[0])
        self.close_connection(con)
        return columns

    def addTableRow(self, tablename):
        columns=self.readTableColumns(tablename)
        command="INSERT INTO "+tablename+" VALUES ("
        for key in enumerate(columns):
            command+="'',"
        command = command[:-1]
        command+=")"

        con=self.connect_database()
        cur= con.cursor()
        try: cur.execute(command)
        except: print("kolize v id")
        con.commit()
        self.close_connection(con)

    def updateTableRow(self, tablename,data):
        columns=self.readTableColumns(tablename)
        command="UPDATE "+tablename+" SET "
        for i,key in enumerate(columns):
            command+=columns[i]+" = ? ,"
        command = command[:-1]
        command+=" WHERE name = ?"

        con=self.connect_database()
        cur = con.cursor()
        try: cur.execute(command,data)
        except: print("kolize v id")
        con.commit()
        self.close_connection(con)

    def deleteTableRow(self, tablename, id):
        con=self.connect_database()
        cur = con.cursor()
        cur.execute("DELETE FROM "+ tablename +" WHERE name=?", (id,))
        con.commit()
        self.close_connection(con)

    def findPK(self, tablename):
        con=self.connect_database()
        cur = con.cursor()
        command="PRAGMA table_info("+tablename+")"
        cur.execute(command)
        tasks = cur.fetchall()
        self.close_connection(con)
        for i,column in enumerate(tasks):
            if column[5]==1:
                return i

        return 0

    def getNewID():
        return str(5)

    def doesIdExist():
        return True
    
    def find_ID_in_database(self, tablename, arg, position):
        list=self.readTableRows(tablename)

        for i,record in enumerate(list):
            if arg==list[i][position]:
                return i

        print("Error-findID didnt find anything arg: "+arg)
        return "ERROR"

    def findIndex(self, keyword, tablename):
        table=self.readTableRows(tablename)
        for i, tableRow in enumerate(table):
            if tableRow[self.findPK(tablename)] == keyword:
                return i 
