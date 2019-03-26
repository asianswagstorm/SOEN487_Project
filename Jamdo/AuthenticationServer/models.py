from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class services(db.Model):
	id = db.Column(db.Integer, unique=True,nullable=False,primary_key=True)
	password = db.Column(db.String(80), nullable=False)
	service = db.Column(db.String(80), nullable=False)
	token = db.Column(db.String(80), nullable=False)	
	def __repr__(self):
		return "<User {}: {} {} {}".format(self.id, self.service, self.email, self.password)

class clients(db.Model):
	id = db.Column(db.Integer, unique=True,nullable=False,primary_key=True)
	email = db.Column(db.String(80), nullable=False)
	username = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)
	token = db.Column(db.Text, nullable=False)
	def __repr__(self):
		return "<Project {}: {} {}".format(self.id, self.name, self.email)
