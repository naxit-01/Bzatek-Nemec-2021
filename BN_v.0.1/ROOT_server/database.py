# loading in modules
import sqlite3
import os

def connect_database(database):

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

