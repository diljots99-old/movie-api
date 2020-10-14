from flask import Flask, render_template, Response, request, flash, redirect, url_for,stream_with_context ,jsonify,send_file
from flask_restful import Api,Resource
from FlaskApp import app
from FlaskApp.database import *
from FlaskApp.apis import Tmdb_api
from FlaskApp.Sources import *
import io
from PIL import Image
import json


class get_people_profile_picture(Resource):
    def get(self,people_id):
        try:
            width = request.args.get("width",None,int)
            api = Tmdb_api()
            myDB = Database()

            people = myDB.get_people_details(people_id)
            if width is None:
                return send_file(io.BytesIO(people["profile_picture"]),mimetype='image/jpeg')
            else:
                image = Image.open(io.BytesIO(people["profile_picture"]))
                imgWidth , imgHeight = image.size

                height = int( (imgHeight / imgWidth) * width)
                image = image.resize((width,height))
            
                byteIO = io.BytesIO()
                image.save(byteIO,format="JPEG")

                imageData = byteIO.getvalue()
                
                return send_file(io.BytesIO(imageData),mimetype='image/jpeg')
        

        except:
            pass
