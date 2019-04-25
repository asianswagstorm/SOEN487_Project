import unittest
import json
from tests.test_main import app as tested_app
from config import TestConfig


tested_app.config.from_object(TestConfig)
tested_app.config['SECRET_KEY'] = 'oh_so_secret'


class TestResourceGathering(unittest.TestCase):
    def setUp(self):
        # nothing to set up
        self.app = tested_app.test_client()


    def tearDown(self):
        #nothing to tear down
        print("one done")

    # ------------------ GET TESTS STARTS ------------------------------

    def test_INVALID_INPUT_for_year_month_day(self):
        # send the request and check the response status code
        response = self.app.get("/death/1948/13/1")
        self.assertEqual(response.status_code, 403)

        # convert the response data from json and call the asserts

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Wrong input of Year, Month or Day"})

    def test_INVALID_INPUT_for_year_month(self):
        # send the request and check the response status code
        response = self.app.get("/death/1823/13/")
        self.assertEqual(response.status_code, 403)

        # convert the response data from json and call the asserts

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Year has to be between 1900 and 2018. Month from 1 to 12"})

    def test_INVALID_INPUT_for_year(self):
        # send the request and check the response status code
        response = self.app.get("/death/1823/")
        self.assertEqual(response.status_code, 403)

        # convert the response data from json and call the asserts

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Year has to be between 1900 and 2018"})


    def test_INVALID_INPUT_for_year_day_month_and_BIRTHS(self):
        # send the request and check the response status code
        response = self.app.get("/birth/2005/11/1")
        self.assertEqual(response.status_code, 403)

        # convert the response data from json and call the asserts

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "There are no important births after 2001"})

    def test_INVALID_INPUT_for_EVENT_TYPE(self):
        # send the request and check the response status code
        response = self.app.get("/birth222/2002/11/1")
        self.assertEqual(response.status_code, 403)

        # convert the response data from json and call the asserts

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "There needs to be an event_type"})

    def test_death_for_year_day_month(self):
        # send the request and check the response status code
        response = self.app.get("/death/1948/1/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts

        death = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(death, {"1948 January 1": " .  Edna May, American actress (b. "})


