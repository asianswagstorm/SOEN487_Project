from flask import Flask
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy is a Object Relational Mapper
from flask_bcrypt import Bcrypt

#dataservice on another port
app = Flask(__name__)
app.secret_key = "super secret key" #needs to be a random secret key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from Jamdo import routes