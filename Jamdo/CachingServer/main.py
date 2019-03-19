from flask import Flask, jsonify, make_response, request
from config import DevConfig

import sqlalchemy


# need an app before we import models because models need it
app = Flask(__name__)
from models import db, row2dict, Result

app.config.from_object(DevConfig)

@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"title": "SOEN487 Assignment 1",
                    "student": {"id": "26795234", "name": "Manuel Toca"}})


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
        if not results

        return make_response(jsonify([row2dict(result) for result in results]))

    results = Result.query.filter_by(year=year, month=month, day=day, location=location, type=type).all()
    if not results

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
        if not results

        return make_response(jsonify([row2dict(result) for result in results]))

    results = Result.query.filter_by(year=year, month=month, location=location, type=type).all()
    if not results

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
        results = Result.query.filter_by(year=year, type=type).all()
        if not results

        return make_response(jsonify([row2dict(result) for result in results]))

    results = Result.query.filter_by(year=year, location=location, type=type).all()
    if not results

    return make_response(jsonify([row2dict(result) for result in results]))


# @app.route("/person")
# def get_all_person():
#     person_list = Person.query.all()
#     return jsonify([row2dict(person) for person in person_list])
#
#
# @app.route("/person/<person_id>")
# def get_person(person_id):
#     # id is a primary key, so we'll have max 1 result row
#     person = Person.query.filter_by(id=person_id).first()
#     if person:
#         return jsonify(row2dict(person))
#     else:
#         return make_response(jsonify({"code": 404, "msg": "Cannot find this person id."}), 404)
#
#
# @app.route("/person", methods={"PUT"})
# def put_person():
#     # get the name first, if no name then fail
#     name = request.form.get("name")
#     if not name:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot put person. Missing mandatory fields."}), 403)
#     person_id = request.form.get("id")
#     if not person_id:
#         p = Person(name=name)
#     else:
#         p = Person(id=person_id, name=name)
#
#     db.session.add(p)
#     try:
#         db.session.commit()
#     except sqlalchemy.exc.SQLAlchemyError as e:
#         error = "Cannot put person. "
#         # print(app.config.get("DEBUG"))
#         if app.config.get("DEBUG"):
#             error += str(e)
#         return make_response(jsonify({"code": 404, "msg": error}), 404)
#     return jsonify({"code": 200, "msg": "success"})
#
#
# @app.route("/person", methods={"POST"})
# def post_person():
#     # get the name first, if no name then fail
#     name = request.form.get("name")
#     if not name:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot post person. Missing mandatory fields."}), 403)
#
#     person_id = request.form.get("id")
#     if not person_id:
#         p = Person(name=name)
#         db.session.add(p)
#     else:
#         # id is a primary key, so we'll have max 1 result row
#         person = Person.query.filter_by(id=person_id).first()
#         if person:
#             person.name = name
#         else:
#             p = Person(id=person_id, name=name)
#             db.session.add(p)
#
#     try:
#         db.session.commit()
#     except sqlalchemy.exc.SQLAlchemyError as e:
#         error = "Cannot post person. "
#         # print(app.config.get("DEBUG"))
#         if app.config.get("DEBUG"):
#             error += str(e)
#         return make_response(jsonify({"code": 404, "msg": error}), 404)
#     return jsonify({"code": 200, "msg": "success"})
#
#
# @app.route("/person/<person_id>", methods={"DELETE"})
# def delete_person(person_id):
#     # id is a primary key, so we'll have max 1 result row
#     person = Person.query.filter_by(id=person_id).first()
#     if person:
#         db.session.delete(person)
#     else:
#         return make_response(jsonify({"code": 404, "msg": "Cannot find this person."}), 404)
#
#     try:
#         db.session.commit()
#     except sqlalchemy.exc.SQLAlchemyError as e:
#         error = "Cannot delete person. "
#         # print(app.config.get("DEBUG"))
#         if app.config.get("DEBUG"):
#             error += str(e)
#         return make_response(jsonify({"code": 404, "msg": error}), 404)
#     return jsonify({"code": 200, "msg": "success"})


if __name__ == '__main__':
    app.run()
