from flask import Flask,render_template,request,abort,session ,flash , jsonify , make_response
from Jamdo.models import User
from Jamdo import app , db, bcrypt
import jwt , datetime
@app.route('/', methods=['GET'])
def root(): 
 
 if not session.get("username"):
  session["username"] = 0
  username = ""
 else:
  username = session["username"]
 return render_template('index.html', username=username) 

@app.route('/login', methods=['GET', 'POST']) 
def login():
 if request.method == "GET":
  return render_template('login.html', title="Register")
 else:
  auth = request.authorization 
  username = request.form.get("u")
  password = request.form.get("p")
  
  if (not username or not password):
   flash("Missing at least one input fields", "danger")
   return make_response(render_template('login.html', title="Login"),500)

  if(User.query.filter_by(username=username).first() is None):
   flash("User " + username + " not found in DB", "danger")
   return  make_response(render_template('login.html', title="Login"),404)
  user = User.query.filter_by(username=username).first()  
  if(not bcrypt.check_password_hash(user.password, password)): #user.password != password
   flash("Incorrect password", "danger")
   return make_response(render_template('login.html', title="Login"),401) #unauthorize status code

  #Create token conditions passed ???
  token = jwt.encode({'iss': "http://localhost:5000/" , 'id' : user.id,'username' : username, 'iat': datetime.datetime.utcnow(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)} ,app.config["SECRET_KEY"])
  session["username"] = username
  session["token"] = token.decode('UTF-8')
  #return jsonify({'token' : token.decode('UTF-8')})
  return make_response(render_template('index.html', username = username), 200)   

@app.route('/register', methods=['GET', 'POST']) 
def register():
 
 if request.method == "GET":
  return render_template('register.html', title="Register")
 else:
  fname = request.form.get("f")
  lname = request.form.get("l")
  username = request.form.get("u")
  password = request.form.get("p") #hash the password
  pw_hash = bcrypt.generate_password_hash(password)

  user_list = User.query.all()
  max_id = 0
  for i in user_list:
   if i.id > max_id:
    max_id = i.id
  if not username or not password or username == "" or password == "" :
   flash("Variable missing, please enter username or password", "danger")
   return make_response(render_template('register.html', title="Register"),404)
  
  if(not User.query.filter_by(username=username).first() is None):
    flash("Username already exists", "danger")
    return make_response(render_template('register.html', title="Register"),500)
  
  new_user =  User(max_id+1,fname,lname,username,pw_hash)
  db.session.add(new_user) 
  db.session.commit() 
  session["username"] = username
  return make_response(render_template('index.html', username = username),200)   
   
@app.route('/logout')
def logout(): 
 session.clear()   
 return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def displayUsers(): 

 if request.method == "GET":
  return render_template('users.html', users = User.query.all())
 else:
   user_id = request.form["id_number"]
   username = request.form["u"]
   if not user_id and not username :
     flash("Invalid Field", "danger")
     return render_template('users.html', users = User.query.all())
   
   elif user_id is not None and not user_id == "": 
    id_to_delete = User.query.filter_by(id=user_id).first()
    db.session.delete(id_to_delete)
   elif username is not None and not username == "": 
    user_to_delete = User.query.filter_by(username=username).first()
    db.session.delete(user_to_delete)
   elif username is not None and user_id is not None:
    id_to_delete = User.query.filter_by(id=user_id).first()
    user_to_delete = User.query.filter_by(username=username).first()
    db.session.delete(id_to_delete)  
    db.session.delete(user_to_delete)

   db.session.commit() 
   return render_template('users.html', users = User.query.all())
      