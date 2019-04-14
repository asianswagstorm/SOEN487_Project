from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Services(db.Model):
	id = db.Column(db.Integer, unique=True,nullable=False,primary_key=True)
	password = db.Column(db.String(80), nullable=False)
	service = db.Column(db.String(80), nullable=False)
	token = db.Column(db.String(80), nullable=False)	
	def __repr__(self):
		return "{{\"id\":{}, \"name\":\"{}\", \"password\":\"{}\", \"token\":\"{}\"}}".format(self.id, self.service, self.password, self.token)
	def serialize(self):
		return {
			'id'         : self.id,
			'service': self.service
		}

class Clients(db.Model):
	id = db.Column(db.Integer, unique=True,nullable=False,primary_key=True)
	email = db.Column(db.String(80), nullable=False)
	username = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)
	token = db.Column(db.Text, nullable=False)
	def __repr__(self):
		return "<Project {}: {} {} {}>".format(self.id, self.name, self.email, self.token)

