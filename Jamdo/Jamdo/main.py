import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy is a Object Relational Mapper
from flask_bcrypt import Bcrypt

from config import Config								# set up config options
import sqlalchemy #SQLAlchemy is a Object Relational Mapper

def get_secret():
	return app.config["SECRET_KEY"]

app = Flask(__name__)									# Enable flask application
app.config.from_object(Config)
bcrypt = Bcrypt(app)

from routes import *

#register server with Auth Server
from authentication import getAuthToken
APPLICATION_AUTH_TOKEN = getAuthToken(app.config['SERVER_AUTH_NAME'],app.config['SERVER_AUTH_PASSWORD'])

if __name__ == "__main__":
    
    app.run(debug=True, port = app.config['SERVER_PORT']) 