import unittest
import json
from main import app as tested_app
from routes_v2 import db as tested_db
from config import TestConfig
from models import Result

tested_app.config.from_object(TestConfig)


class TestResult(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Result(year=1994, type="birth", event="Alice"))
        self.db.session.add(Result(year=1995, type="birth", event="Bob"))
        self.db.session.add(Result(year=1996, month=1, type="birth", event="John"))
        self.db.session.add(Result(year=1997, month=2, day=1, type="birth", event="Ann"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Result.query.delete()
        self.db.session.commit()

    def test_get_all_results(self):
        # send the request and check the response status code
        response = self.app.get("/showDatabase")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(result_list ), list)
        self.assertDictEqual(result_list [0], {"year": "1994", "event": "Alice"})
        self.assertDictEqual(result_list [1], {"year": "1995", "event": "Bob"})

    def test_get_result_with_valid_year(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1994")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(result, {"year": "1994", "type": "birth", "event": "Alice"})

    def test_get_result_with_invalid_year(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/2000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this result."})

    def test_get_result_with_valid_month(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1996/1/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(result, {"year": "1996", "month": "1", "type": "birth", "event": "John"})

    def test_get_result_with_invalid_month(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1996/5/")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this result."})

    def test_get_result_with_valid_day(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1997/2/1/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(result, {"year": "1997", "month": "2", "day": "1", "type": "birth", "event": "Ann"})

    def test_get_result_with_invalid_day(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1997/2/2/")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this result."})

    def test_post_result_without_id(self):
        # do we really need to check counts?
        initial_count = Result.query.filter_by(name="Dan").count()

        # send the request and check the response status code
        response = self.app.post("/person", data={"name": "Dan"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Result.query.filter_by(name="Dan").count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_post_person_new_id(self):
        # do we really need to check counts?
        initial_count = Result.query.filter_by(name="Dan").count()

        # send the request and check the response status code
        response = self.app.post("/person", data={"name": "Dan"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Result.query.filter_by(name="Dan").count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_post_person_with_valid_id(self):
        # do we really need to check counts?
        initial_count = Result.query.filter_by(id="1").count()

        # send the request and check the response status code
        response = self.app.post("/person", data={"id": "1", "name": "Jim"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Result.query.filter_by(id=1).count()
        self.assertEqual(updated_count, initial_count)
