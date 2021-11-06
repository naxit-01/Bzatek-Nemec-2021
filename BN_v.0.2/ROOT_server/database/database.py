# loading in modules
import sqlite3
import os
# Create a SQL connection to our SQLite database 
def connect_database(database):  
    return sqlite3.connect(database) 

def close_connection(con):
    con.close()

def just_load_all(database):
    con = connect_database(database)
    aport=select_all_tasks(con)
    close_connection(con)
    return aport

def select_all_tasks(con):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = con.cursor()
    cur.execute("SELECT * FROM paths")

    rows = cur.fetchall()

    return rows

def sellect_all_columns(con):
    #cursor = con.cursor()
    #data=cursor.execute('''SELECT * FROM table_name''')
    #print(data.description)
    return con.cursor().execute('''SELECT * FROM paths''').description

def create_table(database):
    con=connect_database(database)
    cur = con.cursor()
    cur.execute("""CREATE TABLE admins (
                firstName text,
                lastName text,
                PIN integer
                )""")
    con.commit()
    close_connection(con)
    
def insert_into_table(con):
    

    paths=select_all_tasks(con)
    for i,key in enumerate(paths):
        pass

    cur= con.cursor()
    cur.execute("INSERT INTO paths VALUES ('uistudent','05','128.234.01.02','5000')")
    con.commit()


def find_ID_in_database(database,arg,position):
    con = connect_database(database)
    list=select_all_tasks(con)
    con = close_connection(con)

    for i,record in enumerate(list):
        if arg==list[i][position]:
            return i

    print("Error-findID didnt find anything arg: "+arg)
    return "ERROR"