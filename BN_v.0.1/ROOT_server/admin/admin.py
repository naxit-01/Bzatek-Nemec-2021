from database import database




def admin(db_path, self):

    connection=database.connect_database(db_path)
    
    paths=database.select_all_tasks(connection)
    columns=database.sellect_all_columns(connection)
    
    database.close_connection(connection)
    self.render("mainpage.html", paths=paths, columns=columns, user=True)
    
