from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class API(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(20), nullable=False)
    param = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return "<Person {}: {} {}>".format(self.id, self.name, self.url, self.param)

