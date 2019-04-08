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
    results = Result.query.filter_by(year=year, month=month, day=day, type=event_type).all()
    return make_response(jsonify([row2dict(result) for result in results]))


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected month of year in JSON format
@app.route('/<string:event_type>/<year>/<int:month>/', methods={"GET"})
def return_event_month(event_type, year, month):
    results = Result.query.filter_by(year=year, month=month, type=event_type).all()
    return make_response(jsonify([row2dict(result) for result in results]))


# RETURNS ALL HISTORICAL EVENTS OR DEATHS OR BIRTHS for selected year in JSON format
@app.route('/<string:event_type>/<year>/', methods={"GET"})
def return_event_year(event_type, year):
    results = Result.query.filter_by(year=year, type=event_type).all()
    return make_response(jsonify([row2dict(result) for result in results]))

