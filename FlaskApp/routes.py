from flask import Flask, render_template, Response, request, flash, redirect, url_for,stream_with_context ,jsonify,send_file
from flask_restful import Api,Resource
from FlaskApp import app
from FlaskApp.database import *
from FlaskApp.apis import Tmdb_api
from FlaskApp.Sources import *
import io
from PIL import Image
import json
from FlaskApp.movie import *
from FlaskApp.people import *
api = Api(app)
try:
    SYSTEM_MOVIE_IDS = Database().get_all_movie_ids()
    app.config['SYSTEM_MOVIE_IDS'] =  SYSTEM_MOVIE_IDS

    app.config['SYSTEM_PEOPLE_IDS'] =   Database().get_all_people_ids()
except :
    SYSTEM_MOVIE_IDS = None

class Index(Resource):
    def get(self):
        return jsonify({"status":"OK"})

api.add_resource(Index,"/")
api.add_resource(get_popular_movies,"/get_popular_movies")
api.add_resource(get_top_rated_movies,"/get_top_rated_movies")
api.add_resource(get_now_playing_movies,"/get_now_playing_movies")
api.add_resource(get_movie_poster,"/get_movie_poster/<int:movie_id>")
api.add_resource(get_movie_poster_urls,"/get_movie_poster_urls/<int:movie_id>")
api.add_resource(get_movie_backdrop,"/get_movie_backdrop/<int:movie_id>")
api.add_resource(get_movie_backdrop_urls,"/get_movie_backdrop_urls/<int:movie_id>")
api.add_resource(get_complete_movie_details,"/get_complete_movie_details/<int:movie_id>")
api.add_resource(search_movie,"/search/movie")
api.add_resource(movie_credits,"/movie/credits/<int:movie_id>")

api.add_resource(get_people_profile_picture,"/people/profile_image/<int:people_id>")




@app.route("/config")
def app_config():
    config = app.config
    print(type(config))
    config_json = json.dumps(config,default=str)
    return jsonify(json.loads(config_json))




@app.route("/get_torrent_file/<int:torrent_id>")
def get_torrent_file(torrent_id):
    try:
        MyDB =Database()
        torrent = MyDB.get_torrent_by_id(torrent_id)
        return send_file(io.BytesIO(torrent.get("torrent_file")),mimetype='application/x-bittorrent',attachment_filename=f"{torrent_id}.torrent",as_attachment=True)
    except mysql.connector.errors.InterfaceError as e: 
        print(e._full_msg)
        return jsonify({ "message":"databse error",
            "exception_class": "mysql.connector.errors.InterfaceError",
            "excpection_message": e._full_msg} )




