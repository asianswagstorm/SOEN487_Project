import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Result

tested_app.config.from_object(TestConfig)


class TestResult(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Result(id=1, name="Alice"))
        self.db.session.add(Result(id=2, name="Bob"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Result.query.delete()
        self.db.session.commit()

    def test_get_person_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/person/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        person = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(person, {"id": "1", "name": "Alice"})

    def test_get_person_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/person/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this person id."})

    def test_post_person_without_id(self):
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
