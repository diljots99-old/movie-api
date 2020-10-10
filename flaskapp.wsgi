#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/mysites/FlaskApp/")

from FlaskAppApi import app as application
application.config['secret_key'] = b"akjskajskajs"
application.config['SERVER_NAME'] = 'test.diljotsingh.com'