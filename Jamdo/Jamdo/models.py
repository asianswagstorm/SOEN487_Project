from Jamdo import db 

class User(db.Model):
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable = False)
    lname = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)

    def __init__(self,id,fname,lname,username,password):
        self.id = id
        self.fname = fname 
        self.lname = lname
        self.username = username 
        self.password =  password
        
    def __repr__(self):
        return f"User('{self.username}')"

db.create_all()
