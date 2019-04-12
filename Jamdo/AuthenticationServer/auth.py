from functools import wraps				# decorators
from flask import request, jsonify
import jwt
import datetime
from main import get_secret

# JWT token - https://realpython.com/token-based-authentication-with-flask/
def encode_auth_token(sub):
	try:
		payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365, minutes=10), # ONE YEAR
			'iat': datetime.datetime.utcnow(),
			'sub': sub
		}
		return jwt.encode(
			payload,
			get_secret(),
			algorithm='HS256'
		)
	except Exception as e:
		return e

def decode_auth_token(token):
	auth = {}
	try:
		payload = jwt.decode(token, get_secret())
		auth['payload'] = payload['sub']		
		auth['status'] = 'success'
		auth['message'] = 'Authentication approved of server: ['+payload["sub"]+']'
		return auth
	except jwt.ExpiredSignatureError:
		auth['message'] = 'Authentication token Expired'
		auth['status'] = 'fail'
		auth['payload'] = 'None'		
		return auth
	except jwt.InvalidTokenError:
		auth['status'] = 'fail'
		auth['message'] = 'Authentication token invalid'
		auth['payload'] = 'None'		
		return auth

