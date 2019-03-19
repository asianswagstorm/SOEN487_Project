from main import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    location = db.Column(db.Text)
    type = db.Column(db.Text)
   # local_news = db.Column(db.Text)
   # local_weather = db.Column(db.Text)
   # global_news = db.Column(db.Text)
   # global_weather = db.Column(db.Text)
   # top_movies = db.Column(db.Text)
   # top_albums = db.Column(db.Text)
   # top_books = db.Column(db.Text)
   # births = db.Column(db.Text)
    event = db.Column(db.Text)
   # horoscope = db.Column(db.Text)

    def __repr__(self):
        return "<Result {}: {}>".format(self.id, self.year, self.month, self.day, self.location, self.type, self.event)
        # return "<Results {}: {}>".format(self.id, self.date, self.location, self.local_news, self.local_weather,
        #                                 self.global_news, self.global_weather, self.top_movies, self.top_albums,
        #                                 self.top_books, self.births, self.events, self.horoscope)
