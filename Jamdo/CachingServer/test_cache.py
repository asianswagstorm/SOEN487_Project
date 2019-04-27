import unittest
import json
from main import app as tested_app
#from routes_v2 import db as tested_db
from config import TestConfig
from models import Result, db

tested_app.config.from_object(TestConfig)


class TestResult(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()
        self.main = tested_app.app_context()
        with tested_app.app_context():
            db.init_app(tested_app)  # removes cyclic dependency??
            db.create_all()
            db.session.add(Result(year=1994, type="birth", event="Alice"))
            db.session.add(Result(year=1995, type="death", event="Bob"))
            db.session.add(Result(year=1996, month=1, type="birth", event="John"))
            db.session.add(Result(year=1997, month=2, day=1, type="birth", event="Ann"))
            db.session.commit()

    def tearDown(self):
        # clean up the DB after the tests
        with tested_app.app_context():
            Result.query.delete()
            db.session.commit()

    def test_dump_database(self):
        # send the request and check the response status code
        response = self.app.get("/showDatabase")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(result_list), list)
        self.assertDictEqual(result_list[0], {'id': '1', 'year': '1994', 'day': 'None', 'month': 'None',
                                              'type': 'birth', 'event': 'Alice'})
        self.assertDictEqual(result_list[1], {'id': '2', 'year': '1995', 'month': 'None', 'day': 'None',
                                              'type': 'death', 'event': 'Bob'})

    def test_get_event_year_with_valid_year(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1994/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(result, {'id': '1', 'year': '1994', 'day': 'None', 'month': 'None', 'type': 'birth',
                                      'event': 'Alice'})

    def test_get_event_year_with_invalid_year(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/2000/")
        self.assertEqual(response.status_code, 204)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 204, "msg": "no results"})

    def test_get_event_month_with_valid_month(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1996/1/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(result, {"year": "1996", "month": "1", "type": "birth", "event": "John"})

    def test_get_event_month_with_invalid_month(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1996/5/")
        self.assertEqual(response.status_code, 204)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 204, "msg": "no results"})

    def test_get_event_day_with_valid_day(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1997/2/1/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        result = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(result, {"year": "1997", "month": "2", "day": "1", "type": "birth", "event": "Ann"})

    def test_get_event_day_with_invalid_day(self):
        # send the request and check the response status code
        response = self.app.get("/isCached/birth/1997/2/2/")
        self.assertEqual(response.status_code, 204)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 204, "msg": "no results"})

    def test_post_event_year_without_year(self):
        # send the request and check the response status code
        response = self.app.post("/isCached/birth//")
        self.assertEqual(response.status_code, 403)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Cannot post event. Missing mandatory fields."})

    def test_post_event_year_with_year(self):
        # do we really need to check counts?
        initial_count = Result.query.filter_by(name="Dan").count()

        # send the request and check the response status code
        response = self.app.post("/isCached/birth/1990/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Result.query.filter_by(name="Dan").count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_post_event_month_without_year(self):
        # send the request and check the response status code
        response = self.app.post("/isCached/birth//1/")
        self.assertEqual(response.status_code, 403)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Cannot post event. Missing mandatory fields."})

    def test_post_event_month_with_year(self):
        # do we really need to check counts?
        initial_count = Result.query.filter_by(name="Dan").count()

        # send the request and check the response status code
        response = self.app.post("/isCached/birth/1990/1/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Result.query.filter_by(name="Dan").count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_post_event_day(self):
        # do we really need to check counts?
        initial_count = Result.query.filter_by(id="1").count()

        # send the request and check the response status code
        response = self.app.post("/isCached/birth/1990/1/1/")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Result.query.filter_by(id=1).count()
        self.assertEqual(updated_count, initial_count)
