from flask import Flask, render_template, Response, request, flash, redirect, url_for,stream_with_context ,jsonify,send_file
from flask_restful import Api,Resource
from FlaskApp import app
from FlaskApp.database import *
from FlaskApp.apis import Tmdb_api
from FlaskApp.Sources import *
import io
from PIL import Image
import json

class get_now_playing_movies(Resource):
    def get(self):
        try:
            no_of_pages = request.args.get("no_of_pages",None)
            page_no = request.args.get("page_no",None)
            region = request.args.get("region",None)
            api = Tmdb_api()
            myDb = Database() 
            listOfMovies = []
            for movieJson in  api.get_now_playing_movies(no_of_pages,page_no,region):
                ID = movieJson.get("id")
                result = myDb.get_movies_from_id(ID = ID)

                for movie in result:
                        movie["adult"] = bool(movie.get("adult"))	
                        movie["streamable"] = bool(movie.get("streamable"))	
                        movie["torrent"] = bool(movie.get("torrent"))
                        listOfMovies.append(movie)


            return jsonify({"length":len(listOfMovies),"results":listOfMovies})

        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )

class get_popular_movies(Resource):
    def get(self):
        try:
            no_of_pages = request.args.get("no_of_pages",None)
            page_no = request.args.get("page_no",None)
            region = request.args.get("region",None)
            api = Tmdb_api()
            myDb = Database()   
            listOfMovies = []
            for movieJson in  api.get_popular_movies(no_of_pages,page_no,region):
                ID = movieJson.get("id")
                result = myDb.get_movies_from_id(ID = ID)

                for movie in result:
                        movie["adult"] = bool(movie.get("adult"))	
                        movie["streamable"] = bool(movie.get("streamable"))	
                        movie["torrent"] = bool(movie.get("torrent"))
                        listOfMovies.append(movie)


            return jsonify({"length":len(listOfMovies),"results":listOfMovies})

        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )


class get_top_rated_movies(Resource):
    def get(self):
        try:
            no_of_pages = request.args.get("no_of_pages",None)
            page_no = request.args.get("page_no",None)
            region = request.args.get("region",None)
            api = Tmdb_api()
            myDb = Database()   
            listOfMovies = []
            for movieJson in  api.get_top_rated_movies(no_of_pages,page_no,region):
                ID = movieJson.get("id")
                result = myDb.get_movies_from_id(ID = ID)

                for movie in result:
                        movie["adult"] = bool(movie.get("adult"))	
                        movie["streamable"] = bool(movie.get("streamable"))	
                        movie["torrent"] = bool(movie.get("torrent"))
                        listOfMovies.append(movie)


            return jsonify({"length":len(listOfMovies),"results":listOfMovies})
        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )

class get_movie_poster(Resource):

    def get(self, movie_id):
        try:
            poster_index = request.args.get("poster_index",0,int)
            width = request.args.get("width",None)
            language = request.args.get("language",None)
            if width is None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,poster_index=poster_index)
                if data == None :
                    return jsonify({"message":f"{number_of_poster - 1} can be the highest value of poster_index"})
                else:
                    return send_file(io.BytesIO(data),mimetype='image/jpeg')

            else:
                width = int(width)
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,poster_index=poster_index)
                if data == None :
                    return jsonify({"message":f"{number_of_poster - 1} can be the highest value of poster_index"})
                else:
                    image = Image.open(io.BytesIO(data))
                    imgWidth , imgHeight = image.size

                    height = int((imgHeight / imgWidth) * width)
                    image = image.resize((width,height))
                
                    byteIO = io.BytesIO()
                    image.save(byteIO,format="JPEG")

                    imageData = byteIO.getvalue()
                    
                    return send_file(io.BytesIO(imageData),mimetype='image/jpeg')
        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )

class get_movie_poster_urls(Resource):
    def get(self,movie_id):
        try:
            width = request.args.get("width",None)
            language = request.args.get("language",None)
            
            if width is None and language is None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    url =f"http://www.test.diljotsingh.com/get_movie_poster/{movie_id}?poster_index={i}"
                    listOfUrls.append(url)

                return jsonify(listOfUrls)
            
            if width is not None and language is None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    url =f"http://www.test.diljotsingh.com/get_movie_poster/{movie_id}?poster_index={i}&width={width}"
                    listOfUrls.append(url)

                return jsonify(listOfUrls)
            
            if width is None and language is not None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    url =f"http://www.test.diljotsingh.com/get_movie_poster/{movie_id}?poster_index={i}&language={language}"
                    listOfUrls.append(url)

                return jsonify(listOfUrls)
            
            if width is not None and language is not None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    url =f"http://www.test.diljotsingh.com/get_movie_poster/{movie_id}?poster_index={i}&language={language}&width={width}"
                    listOfUrls.append(url)

                return jsonify(listOfUrls)
        
        except mysql.connector.errors.InterfaceError as e: 
                print(e._full_msg)
                return jsonify({ "message":"databse error",
                    "exception_class": "mysql.connector.errors.InterfaceError",
                    "excpection_message": e._full_msg} )


class get_movie_backdrop(Resource):
    def get(self,movie_id):
        try:
            width = request.args.get("width",None)
            backdrop_index = int(request.args.get("backdrop_index",0))
            
            if width is None:
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id,backdrop_index)
                if data == None :
                    return jsonify({"message":f"{number_of_backdrops - 1} can be the highest value of backdrop_index"})
                else:
                    return send_file(io.BytesIO(data),mimetype='image/jpeg')

            else:
                width = int(width)
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id,backdrop_index)
                if data == None :
                    return jsonify({"message":f"{number_of_backdrops - 1} can be the highest value of backdrop_index"})
                else:
                    image = Image.open(io.BytesIO(data))
                    imgWidth , imgHeight = image.size

                    height = int((imgHeight / imgWidth) * width)
                    image = image.resize((width,height))
                
                    byteIO = io.BytesIO()
                    image.save(byteIO,format="JPEG")

                    imageData = byteIO.getvalue()
                    
                    return send_file(io.BytesIO(imageData),mimetype='image/jpeg')
        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )


class get_movie_backdrop_urls(Resource):
    def get(self,movie_id,width=None):
        try:
            width = request.args.get("width",None)
            if width is None:
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id)
                listOfUrls = []
                for i in range(0,number_of_backdrops):
                    url =f"http://www.test.diljotsingh.com/get_movie_backdrop/{movie_id}?backdrop_index={i}"
                    listOfUrls.append(url)

                return jsonify(listOfUrls)
            else:
                width = int(width)
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id)
                listOfUrls = []
                for i in range(0,number_of_backdrops):
                    url =f"http://www.test.diljotsingh.com/get_movie_backdrop/{movie_id}?backdrop_index={i}&width={width}"
                    listOfUrls.append(url)

                return jsonify(listOfUrls)
        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )


class get_complete_movie_details(Resource):
    def get(self,movie_id):    
        try: 
            width = request.args.get("width",None,int)

            myDB = Database()  
            result = myDB.get_movies_from_id(ID = movie_id)
            api = Tmdb_api()
            myDb = Database()  
            
            if len(result) > 0:
                for movie in result:
                    movie["adult"] = bool(movie.get("adult"))	
                    movie["streamable"] = bool(movie.get("streamable"))
                  
                    movie["backdrop_urls"] = get_movie_backdrop_urls().get(movie_id,width).json
                    movie["torrent"] = bool(movie.get("torrent"))
                    movie["genres"] = myDB.get_movie_genres(ID=movie_id)

                    mySOures = MovieSources()
                    movie["sources"] = mySOures.get_sources(movie_id)


                return jsonify(movie)
            else:
                return jsonify(None)

        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )

class search_movie(Resource):
    def get(self):
        try:
            query = request.args.get("query",None,str)
            language =  request.args.get("language",None,str)
            page =  request.args.get("page",1,int)
            include_adult  =  request.args.get("include_adult",None,bool)
            region  =  request.args.get("region",None,str)
            year =  request.args.get("year",None,int)
            primary_release_year =  request.args.get("primary_release_year",None,int)
            fetch_length = request.args.get("fetch_length",0,int)

            loop_counter = 0
            found_null = 0
            search_result = []
            if query is not None:
                while True:
                    loop_counter == 1
                    api =Tmdb_api()
                    
                
                    for movie in api.search_movie(query,language,page,include_adult,region,year,primary_release_year):
                        if SYSTEM_MOVIE_IDS is not None:
                            if movie.get("id") in SYSTEM_MOVIE_IDS:
                                response = get_complete_movie_details(movie_id=movie.get("id"))
                                if response.json is not None:
                                    search_result.append(response.json)
                                    found_null = 0
                        
                        else:
                            if movie.get("id") in list(Database().get_all_movie_ids()):
                                response = get_complete_movie_details(movie_id=movie.get("id"))
                                if response.json is not None:
                                    search_result.append(response.json)
                                    found_null = 0
                        
                
                    if len(search_result) >= fetch_length or found_null >= 10:
                            break
                    else:
                        page = page + 1
                        found_null += 1



                return jsonify({"total_results":len(search_result),
                                "results":search_result})

        except mysql.connector.errors.InterfaceError as e: 
            print(e._full_msg)
            return jsonify({ "message":"databse error",
                "exception_class": "mysql.connector.errors.InterfaceError",
                "excpection_message": e._full_msg} )

class  movie_credits(Resource):
    def get(self,movie_id):
        # try:
            api = Tmdb_api()
            cast,crew= api.get_movie_credits(movie_id)
            return jsonify({"id":movie_id,"cast":cast,
            "crew":crew})
        # except :
            # pass
