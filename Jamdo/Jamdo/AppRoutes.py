"""
These should be the routes and functions that should be pathway for the servers to communicate to eachother
- each server should, when it runs, register a token with the authentication server
- everything is essentially a placeholder so you don't have to conform to it
- this code is untested
- stuff like: request.args.get('content') is still mostly conceptual, i don't know the datatype or format of the payload

SERVER PORTS:
Application 		default/:80
Authentication 		:200 
Cache 				:300
Resource			:400
"""

from flask import Flask,request,abort,session ,flash , jsonify , make_response,url_for , jwt, json
#
#  ----------Authentication Server----------
#  
# client gets request by REST API
@app.route('/', methods=["POST"])
def createToken():
	server = request.args.get('server')
	password = request.args.get('password')

	# check server and password match, give token

	try:
		payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
			'iat': datetime.datetime.utcnow(),
			'sub': user_id
		}
		# also save token in DB?
		return jwt.encode(
			payload,
			get_secret(),
			algorithm='HS256'
		)
	except Exception as e:
		return e

# client gets request by REST API
@app.route('/checkToken', methods=["Post"])
def checkToken(auth_token):
	token = request.cookies.get('token')
	decoded_token = {}
	if not token:
		decoded_token['message'] = 'Authentication Error: No token. Please Log In'
		return f(decoded_token,*args,**kws)
	else:
		decodedToken = decode_auth_token(token)
	return f(decoded_token,*args,**kws)

def decodeToken(token):
	auth = {}
	try:
		#payload = jwt.decode(auth_token, get_secret())
		#auth['payload'] = payload
		
		# check against db?
		auth['success'] = True
		return auth
	except jwt.ExpiredSignatureError:
		auth['message'] = 'Authentication token Expired. Please Log In.'
		auth['success'] = False
		return auth
	except jwt.InvalidTokenError:
		auth['success'] = False
		auth['message'] = 'Authentication token invalid. Please Log In'
		return auth



#
#  ----------Application Server----------
#  
import requests
SERVER_AUTH_COOKIE = {}
def getAuthToken():
	auth_response = requests.post('localhost:200',server='application',password="AppServerPass")
	if auth_response['success']:
		SERVER_AUTH_COOKIE = auth_response['token']
	else:
		print('Error getting authentication token')

getAuthToken()

# client gets request by REST API
@app.route('/onThisDay/<int:year>/<int:month>/<int:day>', methods=["GET"])
def getDateInformation():
	location = request.args.get('location')		# getting rid of location?

	date = "%d/%d/%d", % (year,month,day) 
	
	cache = checkCachServer(date)
	if(cache['isDataCached']):
		#should return data to HTML templating engine
		return jsonify(content=cache['content'])
	else:
		resource = requestResourceServer(date)
		if resource['success']:
			#should return data to HTML templating engine
			return jsonify(content=cache['content'])
		else
			return jsonify(message=resource['message'])

# client gets request by form submission
@app.route('/onThisDay', methods=["POST"])
def getDateInformationForm():
	location = request.args.get('location')		# getting rid of location?
	year = request.form.get('year')
	month = request.form.get('month')
	day = request.form.get('day')
	
	date = "%d/%d/%d", % (year,month,day) 
	
	cache = checkCachServer(date)
	if(cache['isDataCached']):
		#should return data to HTML templating engine
		return jsonify(content=cache['content'])
	else:
		resource = requestResourceServer(date)
		if resource['success']:
			#should return data to HTML templating engine
			return jsonify(content=cache['content'])
		else
			return jsonify(message=resource['message'])

# always expects json response
def checkCachServer(date):
	# https://stackoverflow.com/questions/15463004/how-can-i-send-a-get-request-from-my-flask-app-to-another-site
	# turns text into JSON object - this required if content-type=app/json?
	return json.loads(requests.get('localhost:300/isCached/'+date, cookie=SERVER_AUTH_COOKIE).content)

def requestResourceServer(date):
	return json.loads(requests.get('localhost:400/getInfo/'+date, cookie=SERVER_AUTH_COOKIE).content)





#
# ------------Caching Server----------------
#

import requests
SERVER_AUTH_COOKIE = {}
def getAuthToken():
	auth_response = requests.post('localhost:200',server='application',password="CacheServerPass")
	if auth_response['success']:
		SERVER_AUTH_COOKIE = auth_response['token']
	else:
		print('Error getting authentication token')

getAuthToken()

@app.route('/isCached/<int:year>/<int:month>/<int:day>', methods=["GET"])
def isDateCached():
	token = request.cookies.get('token');
	auth = requests.post('localhost:200/checkToken',token=token)
	if auth['success']:
		
		# do cache check here
		cache_hit = False 
		cached_content = ''

		if cache_hit:
			return jsonify(success=True,content=cached_content)
		else:
			return jsonify(success=False,message='Date not in Database')
	else:
		return jsonify(success=False,message='Failed Request Authentication')


@app.route('/addResource', methods=["POST"])
def addToDatabase():
	token = request.cookies.get('token');
	auth = requests.post('localhost:200/checkToken',token=token)
	if auth['success']:
		request.args.get('content')
		
		# add to db
		
		success = True
		if success:
			return jsonify(success=True)
		else:
			return jsonify(success=False, message='Failed to add to DB')
	else:
		return jsonify(success=False, message='Failed Request Authentication')





#
# -------------Resource Server-----------
#
import requests
SERVER_AUTH_COOKIE = {}
def getAuthToken():
	auth_response = requests.post('localhost:200',server='application',password="ResourceServerPass")
	if auth_response['success']:
		SERVER_AUTH_COOKIE = auth_response['token']
	else:
		print('Error getting authentication token')

getAuthToken()

@app.route('/getInfo/<int:year>/<int:month>/<int:day>', methods=["GET"])
def getInfo():
	token = request.cookies.get('token');
	auth = requests.post('localhost:200/checkToken',token=token)
	if auth['success']:
		
		# get content
 		gathered_content = ''

		if content:
			cache_data = requests.get('localhost:300/addResource/'+date, cookie=SERVER_AUTH_COOKIE, content=gathered_content)
			if cache_data['success']:
				return jsonify(success=True,content=gathered_content)
			else:
				return jsonify(success=False,message='Couldn\'t cache new resource')
		else:
			return jsonify(success=False,message='Resource Gathering Error')
	else:
		return jsonify(success=False,message='Failed Request Authentication')

