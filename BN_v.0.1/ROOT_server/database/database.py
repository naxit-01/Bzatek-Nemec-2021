# loading in modules
import sqlite3
import os

def connect_database(database):

    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(database) 
    return con

def close_connection(con):
    con.close()


def just_load_all(database):

    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(database)

    aport=select_all_tasks(con)

    con.close()
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

    #for row in rows:
    #    print(row)

    return rows

def sellect_all_columns(con):
    #cursor = con.cursor()
    #data=cursor.execute('''SELECT * FROM table_name''')
    #print(data.description)
    
    return con.cursor().execute('''SELECT * FROM paths''').description