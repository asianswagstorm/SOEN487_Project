import os

from flask import Flask
from config import Config, ServerPasswords				# set up config options

def get_secret():
	return app.config["SECRET_KEY"]

app = Flask(__name__)									# Enable flask application
app.config.from_object(Config)

# Database
from routes import *
with app.app_context():
	db.init_app(app)									# removes cyclic dependency??
	db.create_all()

	#remove previous registrations at startup
	Services.query.delete()

	#register known servers to database
	application_server = Services(password=ServerPasswords.APPLICATION,service="application",token="")
	resource_server = Services(password=ServerPasswords.RESOURCE,service='resource',token="")
	caching_server = Services(password=ServerPasswords.CACHE,service="caching",token="")
	db.session.add(application_server)
	db.session.add(resource_server)
	db.session.add(caching_server)
	
	db.session.commit()

	check_database = Services.query.all()
	print('\n---Content of Auth Server Database---')
	print(check_database,end="\n\n")

if __name__ == "__main__":
	# app.run(debug=True,port=app.config['SERVER_PORT']) 
	app.run()