from functools import wraps				# decorators
from flask import request, jsonify
import jwt
import datetime
from main import get_secret

# JWT token - https://realpython.com/token-based-authentication-with-flask/
def encode_auth_token(user_id):
	try:
		payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365, minutes=10), # ONE YEAR
			'iat': datetime.datetime.utcnow(),
			'sub': user_id
		}
		return jwt.encode(
			payload,
			get_secret(),
			algorithm='HS256'
		)
	except Exception as e:
		return e

def decode_auth_token(auth_token):
	auth = {}
	try:
		payload = jwt.decode(auth_token, get_secret())
		auth['payload'] = payload
		return auth
	except jwt.ExpiredSignatureError:
		auth['message'] = 'Authentication token Expired. Please Log In.'
		return auth
	except jwt.InvalidTokenError:
		auth['message'] = 'Authentication token invalid. Please Log In'
		return auth

# Decorator - checks token on required pages
# https://stackoverflow.com/questions/34495632/how-to-implement-login-required-decorator-in-flask
def protected_endpoint(f):
	@wraps(f)
	def wrapper(*args, **kws):
		token = request.cookies.get('token');
		decoded_token = {}
		if not token:
			decoded_token['message'] = 'Authentication Error: No token. Please Log In'
			return f(decoded_token,*args,**kws)
		else:
			decoded_token = decode_auth_token(token)
		return f(decoded_token,*args,**kws)
	return wrapper