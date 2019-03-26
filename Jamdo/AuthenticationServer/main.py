import os

from flask import Flask
from config import Config								# set up config options

def get_secret():
	return app.config["SECRET_KEY"]

app = Flask(__name__)									# Enable flask application
app.config.from_object(Config)

# Database
from routes import *
with app.app_context():
	db.init_app(app)									# removes cyclic dependency??
	db.create_all()
	db.session.commit()

if __name__ == "__main__":
	app.run(debug=True) 