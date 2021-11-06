from database import database
from tornroutes import route
import tornado.ioloop
import tornado.web



def admin_route(uri, template, db_path, type):
    print("Admin route")
    @route(uri, name=uri)
    class generic_handler(tornado.web.RequestHandler):
        _template = template
        _db_path = db_path
        _type = type
        def args_to_dict(self):
            """ This method converts request arguments to
            usable dict 
            """
            params = self.request.arguments
            for k,v in params.items():
                params[k] = v[0].decode("utf-8")
            return params

        def get(self):

            connection=database.connect_database(self._db_path)

            database.insert_into_table(connection)

            paths=database.select_all_tasks(connection)
            columns=database.sellect_all_columns(connection)
    
            database.close_connection(connection)



            return self.render(self._template, paths=paths, columns=columns, type=self._type)

        def post(self):
            print("POST")
            # This will return all arguments as dict.
            hope=self.request.arguments 
            # Decode the value of each key to str
            # from byte.
            #self.request.arguments[key][0].decode('utf-8')
            # Params as dict.
            params_in_hash = self.args_to_dict()

            if self.get_argument("Edit_button", None) != None:
                
                print("TLACITKO\n")
            
            if self.get_argument("Add_button", None) != None:
                
                print("TLACITKO\n")

    return generic_handler

def admin(db_path, self, type):

    connection=database.connect_database(db_path)

    database.insert_into_table(connection)

    paths=database.select_all_tasks(connection)
    columns=database.sellect_all_columns(connection)
    
    database.close_connection(connection)
    self.render("mainpage.html", paths=paths, columns=columns, user=True, type=type)    

def prototype1_route(uri, template, db_path, type):
    print("Prototype1 route")
    @route(uri, name=uri)
    class generic_handler(tornado.web.RequestHandler):
        _template = template
        _db_path = db_path
        _type = type

        def get(self):
            connection=database.connect_database(self._db_path)

            database.insert_into_table(connection)

            paths=database.select_all_tasks(connection)
            columns=database.sellect_all_columns(connection)
    
            database.close_connection(connection)


            return self.render(self._template, paths=paths, columns=columns, type=self._type)
        def post(self):
            print("button")


    return generic_handler
