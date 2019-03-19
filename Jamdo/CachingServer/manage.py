from main import app
from models import db, Results


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Result=Result)
