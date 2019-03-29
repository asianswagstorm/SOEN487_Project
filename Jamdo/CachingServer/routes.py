from flask import request
from flask import render_template, make_response
from flask import redirect
from flask import jsonify

import datetime

from models import db, Result, row2dict
from main import app

@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"microservice": "Caching Server"})


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected day in month of year in JSON format
@app.route('/<string:event_type>/<year>/<int:month>/<day>', methods={"GET"})
def return_event_day(event_type, year, month, day):
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
        results = Result.query.filter_by(year=year, month=month, day=day, type=type).all()
        if not results:
            return make_response(jsonify([row2dict(result) for result in results]))

    results = Result.query.filter_by(year=year, month=month, day=day, location=location, type=type).all()
    if not results:
        return make_response(jsonify([row2dict(result) for result in results]))


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected month of year in JSON format
@app.route('/<string:event_type>/<year>/<int:month>/', methods={"GET"})
def return_event_month(event_type, year, month):
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
        results = Result.query.filter_by(year=year,month=month, type=type).all()
        if not results:
            return make_response(jsonify([row2dict(result) for result in results]))

    results = Result.query.filter_by(year=year, month=month, location=location, type=type).all()
    if not results:
        return make_response(jsonify([row2dict(result) for result in results]))


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
        results = Result.query.filter_by(year=year, type=event_type).all()
        if not results:
            return make_response(jsonify([row2dict(result) for result in results]))

    results = Result.query.filter_by(year=year, location=location, type=event_type).all()
    if not results:
        return make_response(jsonify([row2dict(result) for result in results]))
