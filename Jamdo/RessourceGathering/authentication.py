# Allows server to register with authentication server
# server is given a token that is used to certify request
from functools import wraps
from flask import request
import requests
import json

def getAuthToken(service, password):

	# Request token from auth server, Auth port:9000
	request_string = 'http://127.0.0.1:9000/getToken?service=' + service + '&password=' + password 
	request_token = requests.Session()
	response = request_token.post(request_string)
	
	# cookies.items returns array of tuples	
	token_value = response.cookies.items()[0][1]
	
	# verify token with auth server
	request_auth_check = requests.Session()
	request_cookie = {'token':token_value}	
	
	response = request_auth_check.post('http://127.0.0.1:9000/authenticate', cookies=request_cookie)
	auth_check = response.json()

	# Confirm registration with Auth Server
	if auth_check['status'] == 'success' and auth_check['payload'] == service:
		print('\n**' + service.upper() + ' Server Registered with Authentication Server**\nToken: [' + token_value + ']\n')
	else:
		print('\n\nERROR: Server not registered with Authentication Server\n\n')
		token_value = '__NO_TOKEN__'

	return token_value if token_value != None else ""

# Decorator - checks token on required pages
# https://stackoverflow.com/questions/34495632/how-to-implement-login-required-decorator-in-flask
def protected_endpoint(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		print('\nAuthenticating request with Authentication Server')
		
		# token belongs to source request
		request_token = request.cookies.get('token');

		# forward token to authentication server to authenticate
		auth_request = requests.Session()
		auth_server_response = auth_request.post('http://127.0.0.1:9000/authenticate', cookies={'token':request_token})
		
		auth = auth_server_response.json()
		
		print('Authentication status: ' + auth['status'], end='\n\n')

		return f(auth,*args,**kwargs)	
	return wrapper