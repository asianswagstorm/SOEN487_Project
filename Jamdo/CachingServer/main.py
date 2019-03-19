from flask import Flask, jsonify, make_response, request
# from config import DevConfig
from sqlalchemy import exists
import sqlalchemy


# need an app before we import models because models need it
app = Flask(__name__)
from models import db, row2dict, Results
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.sqlite'

# app.config.from_object(DevConfig)

@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"title": "SOEN487 Assignment 1",
                    "student": {"id": "26795234", "name": "Manuel Toca"}})

@app.route("/", methods=["GET"])
def get_year():

# @app.route("/person")
# def get_all_person():
#     person_list = Person.query.all()
#     return jsonify([row2dict(person) for person in person_list])
#
#
# @app.route("/person", methods=["DELETE"])
# def delete_all_person():
#     Person.query.delete()
#     person_list = Person.query.all()
#     db.session.commit()
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
# @app.route("/person/<person_id>", methods=["DELETE"])
# def delete_person_by_id(person_id):
#     person = Person.query.filter_by(id=person_id).first()
#     if person:
#         Person.query.filter_by(id=person_id).delete()
#         db.session.commit()
#         return jsonify({"code": 200, "msg": "success"})
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
#         print(app.config.get("DEBUG"))
#         if app.config.get("DEBUG"):
#             error += str(e)
#         return make_response(jsonify({"code": 404, "msg": error}), 404)
#     return jsonify({"code": 200, "msg": "success"})
#
#
# @app.route("/post")
# def get_all_posts():
#     post_list = Post.query.all()
#     return jsonify([row2dict(post) for post in post_list])
#
#
# @app.route("/post", methods=["DELETE"])
# def delete_all_post():
#     Post.query.delete()
#     post_list = Post.query.all()
#     db.session.commit()
#     return jsonify([row2dict(post) for post in post_list])
#
#
# @app.route("/post/<post_id>")
# def get_post(post_id):
#     # id is a primary key, so we'll have max 1 result row
#     post = Post.query.filter_by(post_id=post_id).first()
#     if post:
#         return jsonify(row2dict(post))
#
#
# @app.route("/post/<post_id>", methods=["DELETE"])
# def delete_post_by_id(post_id):
#     post_exists = db.session.query(db.exists().where(Post.post_id == post_id)).scalar()
#     if not post_exists:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Post does not exist."}), 403)
#     post = Post.query.filter_by(post_id=post_id).first()
#     if post:
#         Post.query.filter_by(post_id=post_id).delete()
#         Comment.query.filter_by(post_id=post_id).delete()
#         db.session.commit()
#         return jsonify({"code": 200, "msg": "success"})
#     else:
#         return make_response(jsonify({"code": 404, "msg": "Post does not exist."}), 404)
#
#
# @app.route("/post", methods={"POST"})
# def post_post():
#     content = request.form.get("content")
#     if not content:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot put post. Content is empty."}), 403)
#
#     user_id = request.form.get("user_id")
#     person_id_list = []
#     person_id_list = db.session.query(Person.id).all()
#     if not db.session.query(exists().where(Person.id == user_id)).scalar():
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot put post. User does not exist."}), 403)
#     p = Post(user_id=user_id, content=content)
#     db.session.add(p)
#     try:
#         db.session.commit()
#     except sqlalchemy.exc.SQLAlchemyError as e:
#         error = "Cannot put post. "
#         print(app.config.get("DEBUG"))
#         if app.config.get("DEBUG"):
#             error += str(e)
#         return make_response(jsonify({"code": 404, "msg": error}), 404)
#     return jsonify({"code": 200, "msg": "success"})
#
#
# @app.route("/comment")
# def get_all_comments():
#     comment_list = Comment.query.all()
#     return jsonify([row2dict(comment) for comment in comment_list])
#
#
# @app.route("/comment", methods=["DELETE"])
# def delete_all_comment():
#     Comment.query.delete()
#     comment_list = Comment.query.all()
#     db.session.commit()
#     return jsonify([row2dict(comment) for comment in comment_list])
#
#
# @app.route("/comment/<comment_id>")
# def get_comment(comment_id):
#     comment = Post.query.filter_by(id=comment_id).first()
#     if comment:
#         return jsonify(row2dict(comment))
#
#
# @app.route("/comment/<comment_id>", methods=["DELETE"])
# def delete_comment_by_id(comment_id):
#     comment = Comment.query.filter_by(comment_id=comment_id).first()
#     if comment:
#         Comment.query.filter_by(comment_id=comment_id).delete()
#         db.session.commit()
#         return jsonify({"code": 200, "msg": "success"})
#     else:
#         return make_response(jsonify({"code": 404, "msg": "Comment does not exist."}), 404)
#
#
# @app.route("/comment", methods={"POST"})
# def add_comment():
#     comment = request.form.get("comment")
#     commenter_id = request.form.get("commenter_id")
#     post_id = request.form.get("post_id")
#
#     if not comment:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot put comment. Comment is empty."}), 403)
#
#     person_exists = db.session.query(db.exists().where(Person.id == commenter_id)).scalar()
#     if not person_exists:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot comment on post. User does not exist."}), 403)
#
#     post_exists = db.session.query(db.exists().where(Post.post_id == post_id)).scalar()
#     if not post_exists:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot comment on post. Post does not exist."}), 403)
#     c = Comment(post_id=post_id, commenter_id=commenter_id, comment=comment)
#     db.session.add(c)
#     try:
#         db.session.commit()
#     except sqlalchemy.exc.SQLAlchemyError as e:
#         error = "Cannot put post. "
#         print(app.config.get("DEBUG"))
#         if app.config.get("DEBUG"):
#             error += str(e)
#         return make_response(jsonify({"code": 404, "msg": error}), 404)
#     return jsonify({"code": 200, "msg": "success"})


if __name__ == '__main__':
    app.run()