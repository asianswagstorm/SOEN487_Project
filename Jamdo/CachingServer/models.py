from main import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.Text)
    local_news = db.Column(db.Text)
    local_weather = db.Column(db.Text)
    global_news = db.Column(db.Text)
    global_weather = db.Column(db.Text)
    top_movies = db.Column(db.Text)
    top_albums = db.Column(db.Text)
    top_books = db.Column(db.Text)
    births = db.Column(db.Text)
    events = db.Column(db.Text)
    horoscope = db.Column(db.Text)

    def __repr__(self):
        return "<Results {}: {}>".format(self.id, self.date, self.location, self.local_news, self.local_weather,
                                         self.global_news, self.global_weather, self.top_movies, self.top_albums,
                                         self.top_books, self.births, self.events, self.horoscope)
