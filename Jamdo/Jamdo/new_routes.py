from flask import Flask, render_template, request, abort,session, flash, jsonify, make_response, url_for, redirect
from datetime import date, time
from time import strftime
import requests

from main import app, APPLICATION_AUTH_TOKEN as SERVER_TOKEN

@app.route('/', methods=['GET','POST'])
def getJAMDO(): 
  httpMethod = request.method
  today = str(date.today()) #yyyy-mm-dd
  
  if httpMethod == 'GET':
    return render_template('homepage.html', today=today) 
  
  elif httpMethod == 'POST':
    client_date = request.form.get('date')
    
    parsed_date = client_date.split('-')
    year = parsed_date[0]
    month = parsed_date[1]
    day = parsed_date[2]

    data = ''

    ### check caching server for data ###
    # cache_check = request.get('http://127.0.0.1:7000/year/month/day')
    # cache = cache_check.json()
    cache = {}
    cache['hit'] = 'False'
    cache['data'] = 'akldaf;j'
    
    # get data from cache server
    if cache['hit'] == 'True':
      data = cache['data']
      return render_template('results.html', births=births, deaths=deaths, events=events)         
    
    ### get data from resource server ###
    elif cache['hit'] == 'False':
      cookie = {'token':SERVER_TOKEN}
      
      # Authenticate token at other end
      ext_request = requests.Session()
      get_resource_death = ext_request.get('http://127.0.0.1:5000/death/' + year + '/' + month + '/' + day, cookies=cookie)
      deaths = get_resource_death.json()

      ext_request = requests.Session()
      get_resource_birth = ext_request.get('http://127.0.0.1:5000/birth/' + year + '/' + month + '/' + day, cookies=cookie)
      births = get_resource_birth.json()

      ext_request = requests.Session()
      get_resource_event = ext_request.get('http://127.0.0.1:5000/event/' + year + '/' + month + '/' + day, cookies=cookie)
      events = get_resource_event.json()

      return render_template('results.html', births=births, deaths=deaths, events=events)   
    
    else:
      return render_template('error.html', message='Cache error')

