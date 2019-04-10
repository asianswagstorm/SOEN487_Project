import os

from flask import Flask
from config import Config								# set up config options

def get_secret():
	return app.config["SECRET_KEY"]

app = Flask(__name__)									# Enable flask application
app.config.from_object(Config)

from new_routes import *

#register server with Auth Server
from authentication import getAuthToken
APPLICATION_AUTH_TOKEN = getAuthToken(app.config['SERVER_AUTH_NAME'],app.config['SERVER_AUTH_PASSWORD'])

if __name__ == "__main__":
	app.run(debug=True,port=app.config['SERVER_PORT']) 