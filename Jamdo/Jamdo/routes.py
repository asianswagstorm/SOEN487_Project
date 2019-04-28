from flask import Flask, render_template, request, abort, session, flash, jsonify, make_response, url_for, redirect
from datetime import date, time
from time import strftime
from models import db, User
import jwt, datetime, time, requests, re

from main import app, bcrypt, APPLICATION_AUTH_TOKEN as SERVER_TOKEN

@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)

@app.errorhandler(401)
def incorrect_password(e):
    return make_response(jsonify({"code": 401, "msg": "401: Incorrect password"}), 401)

@app.errorhandler(422)
def incorrect_password(e):
    return make_response(jsonify({"code": 422, "msg": "422: Input Missing"}), 422)

@app.errorhandler(500)
def username_already_exists(e):
    return make_response(jsonify({"code": 500, "msg": "500: Username already exists"}), 500)    


@app.route('/', methods=['GET', 'POST'])
def getJAMDO():
    httpMethod = request.method
    today = str(date.today())  # yyyy-mm-dd

    if 'username' in session and 'fname' in session and 'lname' in session :  
      username = session["username"]
      fname = session["fname"]
      lname = session["lname"]
    else:  
      username = ''
      fname = ''
      lname = ''

    if httpMethod == 'GET':
        return render_template('homepage.html', today=today,fname = fname , lname = lname, username=username)

    elif httpMethod == 'POST':
        client_date = request.form.get('date')  # yyyy-mm-dd

        if (not client_date):
            flash("Date Input Cannot be Blank ", "danger")
            return make_response(render_template('homepage.html', inputError="something",fname = fname , lname = lname, username=username), 500)

        x = re.search("^([12]\d{3}(-(0[1-9]|1[0-2]))*)(-(0[1-9]|[12]\d|3[01]))*$",
                      client_date)  # regex for yyyy-mm-dd, yyyy-mm and yyyy only

        if (not x):
            flash("Invalid Date Format YYYY-MM-DD , YYYY-MM or YYYY only", "danger")
            return make_response(render_template('homepage.html', inputError="something",fname = fname , lname = lname, username=username), 500)

        if (len(client_date) < 8 and len(client_date) > 5):  # month year only
            year = client_date.split("-")[0]
            month = client_date.split("-")[1]
        elif (len(client_date) == 4):  # year only
            year = str(client_date)

        else:  # full date
            parsed_date = client_date.split('-')
            year = parsed_date[0]
            month = parsed_date[1]
            day = parsed_date[2]

        data = ''

        ### check caching server for data ###

        if (len(client_date) < 8 and len(client_date) > 5):
            cache_check1 = requests.Session().get('http://127.0.0.1:5000/isCached/death/' + year + '/' + month)
            deaths = cache_check1.json()
            cache_check2 = requests.Session().get('http://127.0.0.1:5000/isCached/birth/' + year + '/' + month)
            births = cache_check2.json()
            cache_check3 = requests.Session().get('http://127.0.0.1:5000/isCached/event/' + year + '/' + month)
            events = cache_check3.json()

        elif (len(client_date) == 4):
            cache_check1 = requests.Session().get('http://127.0.0.1:5000/isCached/death/' + year)
            deaths = cache_check1.json()
            cache_check2 = requests.Session().get('http://127.0.0.1:5000/isCached/birth/' + year)
            births = cache_check2.json()
            cache_check3 = requests.Session().get('http://127.0.0.1:5000/isCached/event/' + year)
            events = cache_check3.json()

        else:
            cache_check1 = requests.Session().get(
                'http://127.0.0.1:5000/isCached/death/' + year + '/' + month + '/' + day)
            deaths = cache_check1.json()
            cache_check2 = requests.Session().get(
                'http://127.0.0.1:5000/isCached/birth/' + year + '/' + month + '/' + day)
            births = cache_check2.json()
            cache_check3 = requests.Session().get(
                'http://127.0.0.1:5000/isCached/event/' + year + '/' + month + '/' + day)
            events = cache_check3.json()

        no_cache_hit = {"code": 204, "msg": "no results"}
      
        if deaths == births == events == no_cache_hit:
            cookie = {'token': SERVER_TOKEN}
            print("no cache hit")
            # Authenticate token at other end

            ext_request = requests.Session()
            # Year Month Only
            if (len(client_date) < 8 and len(client_date) > 5):
                get_resource_death = ext_request.get('http://127.0.0.1:3000/death/' + year + '/' + month,
                                                     cookies=cookie)
            # Year only
            elif (len(client_date) == 4):
                get_resource_death = ext_request.get('http://127.0.0.1:3000/death/' + year, cookies=cookie)
                # Full date Year Month Day
            else:
                get_resource_death = ext_request.get('http://127.0.0.1:3000/death/' + year + '/' + month + '/' + day,
                                                     cookies=cookie)

            deaths = get_resource_death.json()

            ext_request = requests.Session()
            # Year Month Only
            if (len(client_date) < 8 and len(client_date) > 5):
                get_resource_birth = ext_request.get('http://127.0.0.1:3000/birth/' + year + '/' + month,
                                                     cookies=cookie)
            # Year only
            elif (len(client_date) == 4):
                get_resource_birth = ext_request.get('http://127.0.0.1:3000/birth/' + year, cookies=cookie)
            # Full date Year Month Day
            else:
                get_resource_birth = ext_request.get('http://127.0.0.1:3000/birth/' + year + '/' + month + '/' + day,
                                                     cookies=cookie)
                                                     
            births = get_resource_birth.json()

            ext_request = requests.Session()
            # Year Month Only
            if (len(client_date) < 8 and len(client_date) > 5):
                get_resource_event = ext_request.get('http://127.0.0.1:3000/event/' + year + '/' + month,
                                                     cookies=cookie)
            # Year only
            elif (len(client_date) == 4):
                get_resource_event = ext_request.get('http://127.0.0.1:3000/event/' + year, cookies=cookie)
            # Full date Year Month Day
            else:
                get_resource_event = ext_request.get('http://127.0.0.1:3000/event/' + year + '/' + month + '/' + day,
                                                     cookies=cookie)
            events = get_resource_event.json()

            return render_template('results.html', births=births, deaths=deaths, events=events, comingFrom={"from": "resource"}, fname = fname , lname = lname, username=username)

        elif deaths != no_cache_hit or births != no_cache_hit or events != no_cache_hit:
            print("cache hit")
            return render_template('results.html', births=births, deaths=deaths, events=events, comingFrom={"from": "cache"}, fname = fname , lname = lname, username=username)
        else:
            return render_template('error.html', message='Cache error', fname = fname , lname = lname, username=username)


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
            return make_response(render_template('login.html', inputError="Login"), 422)

        if (User.query.filter_by(username=username).first() is None):
            flash("User " + username + " not found in DB", "danger")
            return make_response(render_template('login.html', inputError="Login"), 404)
        user = User.query.filter_by(username=username).first()
        fname = user.fname
        lname = user.lname
        if (not bcrypt.check_password_hash(user.password, password)):  # user.password != password
            flash("Incorrect password", "danger")
            return make_response(render_template('login.html', inputError="Login"), 401)  # unauthorize status code

        # Create token conditions passed #payload
        token = jwt.encode(
            {'iss': "http://localhost:9000/authenticate", 'id': user.id, 'username': username, 'status': "success",
             'iat': datetime.datetime.utcnow(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
            app.config["SECRET_KEY"])
        session["token"] = token.decode(
            'UTF-8')  # causes problems {'authentication': {'message': 'Unrecognized Token', 'payload': 'None', 'status': 'fail'}}
        session["username"] = username
        session["fname"] = fname
        session["lname"] = lname

        # return jsonify({'token' : token.decode('UTF-8')})
        return make_response(render_template('homepage.html', fname = fname , lname = lname, username=username), 200)

@app.route('/getRandom', methods=['GET'])
def getRandom():
    cached_random = requests.Session().get('http://localhost:5000/getRandom')
    return make_response(jsonify(cached_random.json(),200))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html', title="Register")
    else:
        fname = request.form.get("f")
        lname = request.form.get("l")
        username = request.form.get("u")
        password = request.form.get("p")  # hash the password
        pw_hash = bcrypt.generate_password_hash(password)

        user_list = User.query.all()
        max_id = 0
        for i in user_list:
            if i.id > max_id:
                max_id = i.id
        if not username or not password or username == "" or password == "":
            flash("Variable missing, please enter username or password", "danger")
            return make_response(render_template('register.html', inputError="Register"), 422)

        if (not User.query.filter_by(username=username).first() is None):
            flash("Username already exists", "danger")
            return make_response(render_template('register.html', inputError="Register"), 500)

        new_user = User(max_id + 1, fname, lname, username, pw_hash)
        db.session.add(new_user)
        db.session.commit()
        
        session["username"] = username
        session["fname"] = fname
        session["lname"] = lname
        return make_response(render_template('homepage.html', fname = fname , lname = lname, username=username), 200)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('homepage.html')


@app.route('/users', methods=['GET', 'POST']) #protected route only for admin to manage the users
def displayUsers():

    if (request.method == "GET") :
        if ('username' in session)  and (session["username"] == 'Admin'):
         username =  session["username"]  
         return render_template('users.html', users=User.query.all(), username=username)  
        else:
             return make_response(jsonify({"code": 401,
                                      "msg": "Protected Route only authorized accounts can access this route, Get out of here"}), 401) 
    else:
        user_id = request.form["id_number"]
        Username_Input = request.form["u"]
        if not user_id and not Username_Input:
            flash("Invalid Field", "danger")
            return render_template('users.html', users=User.query.all() , inputError="User", username=session["username"] )
        
        #delete by id
        if user_id is not None and not user_id == "": 
            id_to_delete = User.query.filter_by(id=user_id).first()
            if (id_to_delete == "1") or (user_id == "1") :
             flash("Cannot Delete Admin ", "danger")
             return render_template('users.html', users=User.query.all() , inputError="User", username=session["username"] )
            if id_to_delete is None:
             flash("ID number not in DB ", "danger")
             return render_template('users.html', users=User.query.all() , inputError="User", username=session["username"] )
            elif not id_to_delete == "1":
             db.session.delete(id_to_delete)
        #delete by username
        if Username_Input is not None and not Username_Input == "":
            user_to_delete = User.query.filter_by(username=Username_Input).first()
            if (user_to_delete == session["username"]) or (Username_Input == session["username"]) :
             flash("Cannot Delete Admin ", "danger")
             return render_template('users.html', users=User.query.all() , inputError="User", username=session["username"] )
            if user_to_delete is None :
             flash("Username not in DB ", "danger")
             return render_template('users.html', users=User.query.all() , inputError="User", username=session["username"] )
            elif not user_to_delete == session["username"]:
             db.session.delete(user_to_delete)
  
        db.session.commit()
        return render_template('users.html', users=User.query.all(), username=session["username"] )