import unittest
import json
from main import app as tested_app
# from main import db as tested_db
from config import TestConfig
from models import Result, db

tested_app.config.from_object(TestConfig)


class TestResult(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.app = tested_app.test_client()
        self.main = tested_app.app_context()
        with tested_app.app_context():
            db.init_app(tested_app)  # removes cyclic dependency??
            db.create_all()
            db.session.add(Result(id=1, year=1998, month=5, day=25, type="birth", event="Alice was born."))
            db.session.add(Result(id=2, year=2002, month=11, day=22, type="death", event="Bob died."))
            db.session.add(Result(id=3, year=2012, month=3, day=1, type="event", event="Charles graduated."))
            db.session.add(Result(id=4, year=2002, month=6, day=30, type="death", event="Daniel died."))
            db.session.commit()

    def tearDown(self):
        # clean up the DB after the tests
        with tested_app.app_context():
            Result.query.delete()
            db.session.commit()

    def test_get_valid_result_year(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/death/2002/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(result_list), list)
        self.assertDictEqual(result_list[0], {"id": "2", "year": "2002", "month": "11", "day": "22", "type": "death", "event": "Bob died."})
        self.assertDictEqual(result_list[1], {"id": "4", "year": "2002", "month": "6", "day": "30", "type": "death", "event": "Daniel died."})

    # def test_get_person_with_invalid_id(self):
    #     # send the request and check the response status code
    #     response = self.app.get("/person/1000000")
    #     self.assertEqual(response.status_code, 404)
    #
    #     # convert the response data from json and call the asserts
    #     body = json.loads(str(response.data, "utf8"))
    #     self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this person id."})
    #
    # def test_post_person_without_id(self):
    #     # do we really need to check counts?
    #     initial_count = Result.query.filter_by(name="Dan").count()
    #
    #     # send the request and check the response status code
    #     response = self.app.post("/person", data={"name": "Dan"})
    #     self.assertEqual(response.status_code, 200)
    #
    #     # convert the response data from json and call the asserts
    #     body = json.loads(str(response.data, "utf8"))
    #     self.assertDictEqual(body, {"code": 200, "msg": "success"})
    #
    #     # check if the DB was updated correctly
    #     updated_count = Result.query.filter_by(name="Dan").count()
    #     self.assertEqual(updated_count, initial_count + 1)
    #
    # def test_post_person_new_id(self):
    #     # do we really need to check counts?
    #     initial_count = Result.query.filter_by(name="Dan").count()
    #
    #     # send the request and check the response status code
    #     response = self.app.post("/person", data={"name": "Dan"})
    #     self.assertEqual(response.status_code, 200)
    #
    #     # convert the response data from json and call the asserts
    #     body = json.loads(str(response.data, "utf8"))
    #     self.assertDictEqual(body, {"code": 200, "msg": "success"})
    #
    #     # check if the DB was updated correctly
    #     updated_count = Result.query.filter_by(name="Dan").count()
    #     self.assertEqual(updated_count, initial_count + 1)
    #
    # def test_post_person_with_valid_id(self):
    #     # do we really need to check counts?
    #     initial_count = Result.query.filter_by(id="1").count()
    #
    #     # send the request and check the response status code
    #     response = self.app.post("/person", data={"id": "1", "name": "Jim"})
    #     self.assertEqual(response.status_code, 200)
    #
    #     # convert the response data from json and call the asserts
    #     body = json.loads(str(response.data, "utf8"))
    #     self.assertDictEqual(body, {"code": 200, "msg": "success"})
    #
    #     # check if the DB was updated correctly
    #     updated_count = Result.query.filter_by(id=1).count()
    #     self.assertEqual(updated_count, initial_count)
