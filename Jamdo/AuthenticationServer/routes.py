from flask import request
from flask import render_template, make_response
from flask import redirect
from flask import jsonify
import bcrypt as bcrypt
import datetime

from models import db, User, Project, Files				# get db models

from main import app
from auth import *										#encode, decode, protected endpoint
								
# Authenticate token
@app.route('/authenticate',methods=["POST"])
def checkToken():
	
	return 'Deletion ambiguous'
		
# Displays all User projects
@app.route('/projects',methods=["GET","POST"])
@protected_endpoint
def projects(auth):
	if 'payload' in auth:
		client_id = auth['payload']['sub']
		# display current projects
		if request.method == 'GET':			
			user = User.query.filter_by(id=client_id).first()
			projects = Project.query.filter_by(user_id=user.id).all()
			response = make_response(render_template('projects.html',title=user.username,username=user.username,projects=projects))
			return response

		# add new project
		elif request.method == 'POST':
			project_name = request.form.get('project_name')
			user = User.query.filter_by(id=client_id).first()

			# only add project to appropriate client id from token
			if Project.query.filter_by(user_id=client_id,name=project_name).first() is None:
				new_project = Project(user_id=user.id,name=project_name)
				db.session.add(new_project)
				try:
					db.session.commit()
				except sqlalchemy.exc.SQLAlchemyError as e:
					print(e)
					error = 'Cannot register project'
					return make_response(render_template('/projects',title='Projects',error=error))
				
				# return new list of projects
				projects = Project.query.filter_by(user_id=user.id).all()
				response = make_response(render_template('projects.html',title=user.username,username=user.username,projects=projects))
				return response
			else:
				error = 'Project name already in use'
				return make_response(render_template('projects.html',title='Projects',error=error))
	else:
		response = make_response(render_template('error.html',error=auth['message']))
		return response


# Authentication endpoint - not used - token given at login
# https://medium.com/@riken.mehta/full-stack-tutorial-3-flask-jwt-e759d2ee5727
# https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
@app.route("/api/",methods=["POST"])
def oauth():
	if request.method == 'POST' and request.form:
		username = request.form.get('username')
		password = request.form.get('password')

		user = Clien.query.filter_by(username=username).first()
		hashed_password = user.password

		if user and bcrypt.checkpw(password.encode('utf-8'),hashed_password):		
			# give user new token
			auth_token = encode_auth_token(user.id)				
			return jsonify({'token':auth_token.decode('ascii')}),200
	else:
		return render_template('homepage.html',title='NO AUTH')

@app.errorhandler(404)
def page_not_found(e):
	response = make_response(render_template('404.html'))
	response.status_code = 404
	return response

@app.errorhandler(500)
def internal_error(e):
	response = make_response(render_template('error.html',error="500 Internal Server Error"))
	response.status_code = 500
	return response