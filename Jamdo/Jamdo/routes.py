from flask import Flask,render_template,request,abort,session ,flash , jsonify , make_response,url_for
from Jamdo.config import DevConfig
from RessourceGathering.wiki_parsing import output_data
from datetime import date
from time import strftime
from Jamdo.models import User
from Jamdo import app , db, bcrypt

import jwt, datetime, time

url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext&redirects=1" \
      "&titles="
URL = "https://en.wikipedia.org/w/api.php"

monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
             7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


@app.route('/', methods=['GET'])
def root(): 
 today = str(date.today()) #yyyy-mm-dd
 if not session.get("username"):
  session["username"] = 0
  username = ""
 else:
  username = session["username"]
 return render_template('index.html', username=username ,today=today) 


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected day in month of year in JSON format
@app.route('/getEvent', methods=['GET']) #Change the route please help me
def return_event_day():
 today = str(date.today()) 
 event_type = request.args.get("event_type")
 request_date = request.args.get("date")
 year=request_date.split("-")[0]
 month= int(request_date.split("-")[1])
 day= request_date.split("-")[2]

 if int(year) < 1900 or int(year) > 2018:
     return make_response(jsonify({"code": 403,
                                   "msg": "Year has to be between 1900 and 2018"}), 403)
 if event_type == "event":
     type = 1
 elif event_type == "birth":
     if int(year) >= 2002:
         return make_response(jsonify({"code": 403,
                                       "msg": "There are no important births after 2001"}), 403)
     type = 2
 elif event_type == "death":
     type = 3
     if int(year) >= 2002:
         type = 2
 else:
     return make_response(jsonify({"code": 403,
                                   "msg": "There needs to be an event_type"}), 403)
 
 result = output_data(year, month, day, type)
 result = output_data(year, month, day, type)
 key = str(year) + " " + monthDict[month]+ " " + str(day)

 if key in result:
  return make_response(jsonify({key: result[key]}),200)
 else:
  return make_response(jsonify({"code": 403,
                                "msg": "There is no information for that date"}), 403) 


#YEAR AND MONTH ONLY
# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected month of year in JSON format
@app.route('/<string:event_type>/<year>/<int:month>/', methods={"GET"})
def return_event_month(event_type, year, month):
    # location = request.args.get("location")
    type = 0
    if int(year) < 1900 or int(year) > 2018:
        return make_response(jsonify({"code": 403,
                                      "msg": "Year has to be between 1900 and 2018"}), 403)
    if event_type == "event":
        type = 1
    elif event_type == "birth":
        if int(year) >= 2002:
            return make_response(jsonify({"code": 403,
                                          "msg": "There are no important births after 2001"}), 403)
        type = 2
    elif event_type == "death":
        type = 3
        if int(year) >= 2002:
            type = 2
    else:
        return make_response(jsonify({"code": 403,
                                      "msg": "There needs to be an event_type"}), 403)

    result = output_data(year, month, 0, type)
    return make_response(jsonify(result))


#YEAR ONLY
# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected year in JSON format
@app.route('/<string:event_type>/<year>/', methods={"GET"})
def return_event_year(event_type, year):
    location = request.args.get("location")
    type = 0
    if int(year) <1900 or int(year) > 2018:
        return make_response(jsonify({"code": 403,
                                      "msg": "Year has to be between 1900 and 2018"}), 403)
    if event_type == "event":
        type = 1
    elif event_type == "birth":
        if int(year) >= 2002:
            return make_response(jsonify({"code": 403,
                                          "msg": "There are no important births after 2001"}), 403)
        type = 2
    elif event_type == "death":
        type = 3
        if int(year) >= 2002:
            type = 2
    else:
        return make_response(jsonify({"code": 403,
                                      "msg": "There needs to be an event_type"}), 403)

    if not location:
        result = output_data(year, 1, 0, type)
    result = output_data(year, 1, 0, 1) ## for january
    for i in range(2, 13):
        nextMonth = output_data(year, i, 0, type)
        ##print(nextMonth)
        if nextMonth:
            result.update(nextMonth)
    return jsonify(result)


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
      