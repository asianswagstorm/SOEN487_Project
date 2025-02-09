from flask import Flask, jsonify, make_response, request
from config import DevConfig
import sqlalchemy

# need an app before we import models because models need it
app = Flask(__name__)

app.config.from_object(DevConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from routes import *
with app.app_context():
    db.init_app(app)									# removes cyclic dependency??
    db.create_all()
    # db.session.add(Result(id=1, year=1990, month=11, day=3, location="Montreal", type="birth", event="bla"))
    # db.session.add(Result(id=2, year=2000, month=2, day=2, location="Montreal", type="birth", event="bla"))
    db.session.commit()

#register server with Auth Server
from authentication import getAuthToken
APPLICATION_AUTH_TOKEN = getAuthToken(app.config['SERVER_AUTH_NAME'],app.config['SERVER_AUTH_PASSWORD'])

if __name__ == '__main__':
    app.run(port=app.config['SERVER_PORT'])
