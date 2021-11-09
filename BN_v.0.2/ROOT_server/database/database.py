import sqlite3
# Create a SQL connection to our SQLite database 
def connect_database(database):  
    return sqlite3.connect(database) 

def close_connection(con):
    con.close()

def readTableNames(database):
    con=connect_database(database)
    res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablenames = []
    for name in res.fetchall():
        tablenames.append(name[0])
    close_connection(con)
    return tablenames

def readTableRows(database, tablename):
    con=connect_database(database)
    cur=con.cursor()
    query = "SELECT * FROM "+tablename
    cur.execute(query)
    tasks = cur.fetchall()
    close_connection(con)
    return tasks

def readTableColumns(database, tablename):
    con=connect_database(database)
    cur=con.cursor()
    res=cur.execute("SELECT * FROM "+tablename).description
    columns =[]
    for name in res:
        columns.append(name[0])
    close_connection(con)
    return columns

def addTableRow(database, tablename):
    columns=readTableColumns(database, tablename)
    command="INSERT INTO "+tablename+" VALUES ("
    for key in enumerate(columns):
        command+="'',"
    command = command[:-1]
    command+=")"

    con=connect_database(database)
    cur= con.cursor()
    try: cur.execute(command)
    except: print("kolize v id")
    con.commit()
    close_connection(con)

def updateTableRow(database, tablename,data):
    columns=readTableColumns(database, tablename)
    command="UPDATE "+tablename+" SET "
    for i,key in enumerate(columns):
        command+=columns[i]+" = ? ,"
    command = command[:-1]
    command+=" WHERE id = ?"

    con=connect_database(database)
    cur = con.cursor()
    try: cur.execute(command,data)
    except: print("kolize v id")
    con.commit()
    close_connection(con)

def deleteTableRow(database, tablename, id):
    con=connect_database(database)
    cur = con.cursor()
    cur.execute("DELETE FROM "+ tablename +" WHERE id=?", (id,))
    con.commit()
    close_connection(con)

def findPK(database, tablename):
    con=connect_database(database)
    cur = con.cursor()
    command="PRAGMA table_info("+tablename+")"
    cur.execute(command)
    tasks = cur.fetchall()
    close_connection(con)
    for i,column in enumerate(tasks):
        if column[5]==1:
            return i

    return 0

def getNewID():
    return str(5)

def doesIdExist():
    return True
    
def find_ID_in_database(database, tablename, arg,position):
    con = connect_database(database)
    list=readTableRows(database, tablename)
    con = close_connection(con)

    for i,record in enumerate(list):
        if arg==list[i][position]:
            return i

    print("Error-findID didnt find anything arg: "+arg)
    return "ERROR"
