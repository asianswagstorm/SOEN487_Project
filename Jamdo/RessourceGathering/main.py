from flask import Flask, jsonify, make_response, request, url_for, redirect, render_template, flash, json
from wiki_parsing import output_data
from movie_parsing import output_top_movie
from config import DevConfig

import requests
import sqlalchemy

# need an app before we import models because models need it
app = Flask(__name__)
app.config.from_object(DevConfig)
app.config['SECRET_KEY'] = 'oh_so_secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
##from models import db, row2dict, API


url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext&redirects=1" \
      "&titles="
URL = "https://en.wikipedia.org/w/api.php"

monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
             7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"microservice": "resource gathering"})

# CAN ONLY SEARCH FROM 1900 to NOW


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected day in month of year in JSON format
@app.route('/<string:event_type>/<year>/<int:month>/<day>', methods={"GET"})
def return_event_day(event_type, year, month, day):

    cache_url = "http://127.0.0.1:5000/isCached/" + event_type + "/" + year + "/" + str(month) + "/" + day + "/"
    r = requests.Session()
    cache_response = r.get(cache_url)

    # If search query not in cache
    # if cache_response.json() == {"code": 204, "msg": "no results"}:
    location = request.args.get("location")

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

    # if not location:
    #     result = output_data(year, month, day, type)

    result = output_data(year, month, day, type)

    key = str(year) + " " + monthDict[month]+ " " + str(day)

    # cache_url = "http://127.0.0.1:5000/" + year + "/" + str(month) + "/" + day + "/"
    # res = r.post(cache_url, data=result)
    # make_response(jsonify({key: result[key]}))
    # return make_response(jsonify({"code": 403,
    #                               "msg": "There is no information for that date"}), 403)

    if key in result:
        # cache_url = "http://127.0.0.1:5000/" + year + "/" + str(month) + "/" + day + "/"
        r = requests.Session()
        r.post(cache_url, data=json.dumps(result[key]))
        return make_response(jsonify({key: result[key]}))
    else:
        return make_response(jsonify({"code": 403,
                                      "msg": "There is no information for that date"}), 403)
    # If search query in cache
    # else:
    #     return jsonify(cache_response.json())
        #return "There already"

# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected month of year in JSON format
@app.route('/<string:event_type>/<year>/<int:month>/', methods={"GET"})
def return_event_month(event_type, year, month):

    cache_url = "http://127.0.0.1:5000/isCached/" + event_type + "/" + year + "/" + str(month) + "/"
    r = requests.Session()
    cache_response = r.get(cache_url)

    # If search query not in cache
    # if cache_response.json() == {"code": 204, "msg": "no results"}:
    location = request.args.get("location")
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
    if not location:
        result = output_data(year, month, 0, type)
    result = output_data(year, month, 0, type)

    result1 = json.dumps(result)
    res = r.post(cache_url, data=result1)
    return make_response(jsonify(result))
    # else:
    #     return jsonify(cache_response.json())


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected year in JSON format
@app.route('/<string:event_type>/<year>/', methods={"GET"})
def return_event_year(event_type, year):

    cache_url = "http://127.0.0.1:5000/isCached/" + event_type + "/" + year + "/"
    r = requests.Session()
    cache_response = r.get(cache_url)

    # If search query not in cache
    # if cache_response.json() == {"code": 204, "msg": "no results"}:
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
    result1 = json.dumps(result)
    res = r.post(cache_url, data=result1)
    return make_response(jsonify(result))

    # If search query in cache
    # else:
    #     return jsonify(cache_response.json())


@app.route('/movie/top/<int:number>', methods={"GET"})
def return_top_movies(number):
    if number <= 0 or number > 200:
        return make_response(jsonify({"code": 403,
                                      "msg": "Number of movies needs to be higher than 0 or smaller than 200"}), 403)
    result = output_top_movie(number)
    return jsonify(result)


# -------------------------     END SETUP SECTION   ------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=app.config['SERVER_PORT'])
