from flask import request
from flask import render_template, make_response
from flask import redirect
from flask import jsonify, json

import datetime

from models import db, Result, row2dict
from main import app


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"microservice": "Caching Server"})


# DUMP entire database
@app.route('/showDatabase', methods={"GET"})
def dump_database():
    result_list = Result.query.all()
    return jsonify([row2dict(result) for result in result_list])


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected day in month of year in JSON format
@app.route('/<year>/<int:month>/<day>', methods={"GET", "POST"})
def return_event_day(year, month, day):
    httpmethod = request.method
    if httpmethod == "GET":
        results = Result.query.filter_by(year=year, month=month, day=day).all()
        if not results:
            return jsonify({"code": 204, "msg": "no results"})
        return make_response(jsonify([row2dict(result) for result in results]))

    if httpmethod == "POST":
        # get the year first, if no year then fail
        year = request.args.get('year')
        if not year:
            return make_response(jsonify({"code": 403,
                                          "msg": "Cannot post event. Missing mandatory fields."}), 403)

        month = request.args.get('month')
        day = request.args.get('day')

        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December',
                      13: 'Nobel Prizes'}
        month_name = month_dict[month]

        # get the events JSON string and parse into a Python string
        content = request.get_json
        events = json.loads(content)

        if not month and not day:
            r = Result(year=year, event=event)
        elif not month:
            r = Result(year=year, event=event)
        elif not day:
            r = Result(year=year, month=month_name, event=event)
        else:
            r = Result(year=year, month=month_name, day=day, event=event)

        db.session.add(r)
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot put person. "
            # print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "success"})


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected month of year in JSON format
@app.route('/<year>/<int:month>/', methods={"GET", "POST"})
def return_event_month(year, month):
    httpmethod = request.method
    if httpmethod == "GET":
        results = Result.query.filter_by(year=year, month=month).all()
        if not results:
            return jsonify({"code": 204, "msg": "no results"})
        return make_response(jsonify([row2dict(result) for result in results]))

    if httpmethod == "POST":
        # get the year first, if no year then fail
        year = request.args.get('year')
        if not year:
            return make_response(jsonify({"code": 403,
                                          "msg": "Cannot post event. Missing mandatory fields."}), 403)

        month = request.args.get('month')

        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December',
                      13: 'Nobel Prizes'}

        month_name = month_dict[month]

        # get the events JSON string and parse into a Python string
        content = request.get_json
        event = json.loads(content)

        if not month:
            r = Result(year=year, event=event)
        else:
            r = Result(year=year, month=month_name, event=event)

        db.session.add(r)
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot put person. "
            # print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "success"})


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected year in JSON format
@app.route('/<year>/', methods={"GET", "POST"})
def return_event_year(year):
    httpmethod = request.method
    if httpmethod == "GET":
        results = Result.query.filter_by(year=year).all()
        if not results:
            return jsonify({"code": 204, "msg": "no results"})
        return make_response(jsonify([row2dict(result) for result in results]))

    if httpmethod == "POST":
        # get the year first, if no year then fail
        year = request.args.get('year')

        if not year:
            return make_response(jsonify({"code": 403,
                                          "msg": "Cannot post event. Missing mandatory fields."}), 403)

        # get the events JSON string and parse into a Python string

        content = request.get_json
        event = json.loads(content)

        r = Result(year=year, event=event)
        db.session.add(r)
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot put person. "
            # print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "success"})

