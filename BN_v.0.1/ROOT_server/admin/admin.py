from database import database
import tornado



def admin(db_path, self, type):


    connection=database.connect_database(db_path)

    database.insert_into_table(connection)

    paths=database.select_all_tasks(connection)
    columns=database.sellect_all_columns(connection)
    
    database.close_connection(connection)
    self.render("mainpage.html", paths=paths, columns=columns, user=True, type=type)
    self.redirect(tornado.httputil.url_concat("http://127.0.0.1:5000" + "/admin", 
			[("response_type","code"), 
			("scope","profile")]))
    
