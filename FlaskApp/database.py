import mysql.connector
from FlaskApp import app
import binascii

class Database:
    def __init__(self,host=app.config['DB_HOST'],port=app.config['DB_PORT'],user=app.config['DB_USERNAME'],password=app.config['DB_PASSWORD'],dbname=app.config['DB_NAME']):
        
        self.mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            auth_plugin='mysql_native_password'

        )



    def get_movies(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM movies LIMIT  20;")
        listOfMovies = mycursor.fetchall()

        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW COLUMNS FROM movies")
        columns = mycursor.fetchall()
        columnsKEYS = []
        for column in columns:
            columnsKEYS.append(column[0])
        
        columnsKEYS = tuple(columnsKEYS)

        listOfMovieDict = []
        for movie in listOfMovies:
            movieDICT = dict(zip(columnsKEYS,movie))
            listOfMovieDict.append(movieDICT)
        return listOfMovieDict

    def get_all_movies(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM movies;")
        listOfMovies = mycursor.fetchall()

        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW COLUMNS FROM movies")
        columns = mycursor.fetchall()
        columnsKEYS = []
        for column in columns:
            columnsKEYS.append(column[0])
        
        columnsKEYS = tuple(columnsKEYS)

        listOfMovieDict = []
        for movie in listOfMovies:
            movieDICT = dict(zip(columnsKEYS,movie))
            listOfMovieDict.append(movieDICT)
        return listOfMovieDict

    def get_movies_from_id(self,ID=None):
        if ID is not None:
            mycursor = self.mydb.cursor()
            mycursor.execute(f"SELECT * FROM movies where id={ID};")
            listOfMovies = mycursor.fetchall()

            mycursor = self.mydb.cursor()
            mycursor.execute("SHOW COLUMNS FROM movies")
            columns = mycursor.fetchall()
            columnsKEYS = []
            for column in columns:
                columnsKEYS.append(column[0])
            
            columnsKEYS = tuple(columnsKEYS)

            listOfMovieDict = []
            for movie in listOfMovies:
                movieDICT = dict(zip(columnsKEYS,movie))
                listOfMovieDict.append(movieDICT)

            return listOfMovieDict

        else:
            return None
    def get_movie_genres(self,ID= None):
        if ID is not None:
            mycur= self.mydb.cursor()
            sql = f"SELECT * FROM `movies_to_genres` where movie_id={ID};"
            mycur.execute(sql)
            print()
            listOfgenres = mycur.fetchall()

            listOfGeres_Dict = []

            for genres in listOfgenres:
                
                mycursor = self.mydb.cursor()
                mycursor.execute(f"SELECT * FROM genres where id={genres[1]};")
                gen = mycursor.fetchall()

                for row in gen:
                    
               
                    listOfGeres_Dict.append ({
                        "id" :row[0],
                        "name":row[1]
                    })

            return listOfGeres_Dict

    def get_movies_torrents(self,ID= None):
        if ID is not None:
            mycur= self.mydb.cursor()
            sql = f"SELECT * FROM `movies_to_torrents` where movie_id={ID};"
            mycur.execute(sql)
            print()
            listOftorrents = mycur.fetchall()

            listOftorrents_DICT = []

            mycursor = self.mydb.cursor()
            mycursor.execute("SHOW COLUMNS FROM torrents")
            columns = mycursor.fetchall()
            columnsKEYS = []
            for column in columns:
                columnsKEYS.append(column[0])

            columnsKEYS = tuple(columnsKEYS)

            for torrent in listOftorrents:
                
                mycursor = self.mydb.cursor()
                mycursor.execute(f"SELECT * FROM torrents where id={torrent[1]};")
                gen = mycursor.fetchall()

                for row in gen:
                    torrentDICT = dict(zip(columnsKEYS,row))
                    torrentDICT.pop('torrent_file')
                    listOftorrents_DICT.append(torrentDICT)


            return listOftorrents_DICT

    def get_torrent_by_id(self,torren_id):
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW COLUMNS FROM torrents")
        columns = mycursor.fetchall()
        columnsKEYS = []
        for column in columns:
            columnsKEYS.append(column[0])

        columnsKEYS = tuple(columnsKEYS)

        mycursor = self.mydb.cursor()
        mycursor.execute(f"SELECT * FROM torrents where id={torren_id};")
        gen = mycursor.fetchall()

        for row in gen:
            torrentDICT = dict(zip(columnsKEYS,row))
            
            
        return torrentDICT

    def add_genre(self,id,name):
        try:
                
            mycursor = self.mydb.cursor()
            columns = ', '.join(["id","name"])
            placeholders = ', '.join(['%s'] * 2)
            sql = "INSERT INTO %s ( %s ) VALUES (  %s );" % ('genres', columns, placeholders)
            values = tuple( [id,name])
                
            mycursor.execute(sql , values)

            self.mydb.commit()
        except :
            pass

    def add_movies_to_genres(self,movie_id,genre_id):
        try:
                
            mycursor = self.mydb.cursor()
            columns = ', '.join(["movie_id","genre_id"])
            placeholders = ', '.join(['%s'] * 2)
            sql = "INSERT INTO %s ( %s ) VALUES (  %s );" % ('movies_to_genres', columns, placeholders)
            values = tuple( [movie_id,genre_id])
                
            mycursor.execute(sql , values)

            self.mydb.commit()
        except :
            pass

    def update_movie(self,id,vote_average,vote_count,popularity):
        try:
            sql = f"UPDATE movies set vote_average={vote_average} , vote_count={vote_count} ,popularity={popularity} where id={id};"

            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            self.mydb.commit()

        except :
            pass
        
    def get_all_movie_ids(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT id FROM movies;")
        listOfMovies = mycursor.fetchall()
        RESULT = []
        for ID in listOfMovies:
            RESULT.append(ID[0])
        return RESULT

    def add_people(self,people_json,profile_picture=None):
        try:
            mycursor = self.mydb.cursor()
            list_of_columns = ["id","birthday","known_for_department","death_day","name","gender","popularity","imdb_id","homepage","place_of_birth","profile_picture","biography","adult"]
            list_of_values = [people_json.get("id"),people_json.get("birthday"),people_json.get("known_for_department"),people_json.get("death_day"),
            people_json.get("name"),people_json.get("gender"),people_json.get("popularity"),people_json.get("imdb_id"),people_json.get("homepage"),people_json.get("place_of_birth"),profile_picture,people_json.get("biography"),people_json.get("adult")]
            
            columns = ', '.join(list_of_columns)
            placeholders = ', '.join(['%s'] * len(list_of_columns))
            
            sql = "INSERT INTO %s ( %s ) VALUES (  %s );" % ('people', columns, placeholders)
            
            values = tuple( list_of_values)
                
            mycursor.execute(sql , values)

            self.mydb.commit()
        except:
            pass