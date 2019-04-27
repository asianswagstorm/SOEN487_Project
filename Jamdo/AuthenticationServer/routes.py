from flask import request
from flask import render_template, make_response
from flask import redirect
from flask import jsonify
import bcrypt as bcrypt
import datetime
import json

from models import db, Services				# get db models

from main import app
from auth import *										#encode, decode, protected endpoint
								
@app.route('/',methods=["GET"])
def root():
	return jsonify({"microservice": "Authentication Server"})

@app.route('/showDatabase',methods=["GET"])
def showData():
	data = Services.query.all()
	return render_template('response.html',data=data)

# Authenticate token
@app.route('/getToken',methods=["POST"])
def getToken():
	# assume these arguments are encrypted across a network
	service = request.args.get('service')
	password = request.args.get('password')
	
	"""
	# put hashed password in auth server DB
	hashed_password = 

	# encrypt password
	if service and bcrypt.checkpw(password.encode('utf-8'),hashed_password):		
		auth_token = encode_auth_token(user.id)				
	"""

	result_set = Services.query.filter_by(service=service,password=password).first()
	print(result_set)
	if result_set == None:
		return jsonify(
				status="fail",
				message="Client Unknown"				
			)
	else:
		token = encode_auth_token(service)
		result_set.token = token
		db.session.commit()

		response = make_response(jsonify(
				status="success",			
				token=str(token,'utf-8')
			))

		# Put token in client cookie
		response.set_cookie('token',str(token))
		return response


# client gets request by REST API
@app.route('/authenticate', methods=["Post"])
def authToken():
	token = request.cookies.get('token')
	decoded_token = {}

	# check for token/cookie
	if not token:
		decoded_token['status'] = 'fail'
		decoded_token['message'] = 'No Token'
		decoded_token['payload'] = 'None'
	else:
		result_set = Services.query.all()
		decoded_token['status'] = 'fail'
		decoded_token['message'] = 'Unrecognized Token'
		decoded_token['payload'] = 'None'

		for service in result_set:
			# token found
			if str(service.token) == token:
				# decode won't accept token as string, use DB byte string
				decoded_token = decode_auth_token(service.token)
		
	return jsonify(status=decoded_token['status'],message=decoded_token['message'],payload=decoded_token['payload'])

@app.errorhandler(404)
def page_not_found(e):
	response = make_response(jsonify(status='404 Not Found'))
	response.status_code = 404
	return response

@app.errorhandler(500)
def internal_error(e):
	response = make_response(jsonify(status='500 Internal Server Error'))
	response.status_code = 500
	return response