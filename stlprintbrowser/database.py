from tinydb import TinyDB

class STL_Database:

    def __init__(self,settings):
        self.db = TinyDB(settings.database_path+'/stldatabase.json')