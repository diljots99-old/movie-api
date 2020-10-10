from flask import Flask
from flask_cors import CORS

app = Flask (__name__)

cors = CORS(app)

app.config['secret_key'] = b"akjskajskajs"

# app.config['DB_HOST']=  "15.207.253.57"
app.config['DB_HOST']=  "localhost"

# app.config['DB_HOST']=  "www.diljotsingh.com"

app.config['DB_PORT'] = "3306"
app.config['DB_USERNAME'] = "admin"
app.config['DB_PASSWORD'] = "Password@123"
app.config['DB_NAME'] = "dj"






# app.config['SERVER_NAME'] = 'test.diljotsingh.com'

from FlaskApp import routes

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#   return response