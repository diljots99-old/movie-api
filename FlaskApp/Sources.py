from FlaskApp.database import *
from FlaskApp.apis import Tmdb_api
from FlaskApp.Sources import *

class MovieSources():
    def __init__(self):
        pass


    def get_torrets(self,moive_id):
        MyDB = Database()

        listOfTosrrent = MyDB.get_movies_torrents(moive_id)
        return listOfTosrrent
            
    def get_sources(self,moive_id):
        torrents = self.get_torrets(moive_id)
        sources = {}
        if len(torrents) > 0:
            sources["torrents"] = torrents 

        return sources