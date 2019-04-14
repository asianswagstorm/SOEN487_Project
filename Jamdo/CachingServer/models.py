# from main import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    type = db.Column(db.Text)
    event = db.Column(db.Text)

    # def __init__(self, id, year, month, day, location, type, event):
    #     self.id = id
    #     self.year = year
    #     self.month = month
    #     self.day = day
    #     self.type = type
    #     self.event = event

    def __repr__(self):
        return "<Result {}: {}>".format(self.id, self.year, self.month, self.day, self.type, self.event)

