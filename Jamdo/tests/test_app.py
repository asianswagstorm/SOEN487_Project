import unittest
import json
from Jamdo.main import app as Jamdo_app
from Jamdo.config import TestConfig

Jamdo_app.config.from_object(TestConfig)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()

    def test_404_on_invalid_url(self):
        # send the request and check the response status code
        response = self.app.get("/something")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "404: Not Found"})

    def test_root(self):
        # send the request and check the response status code
        response1 = self.app.get("http://127.0.0.1:3000/") #ResourceGathering
        self.assertEqual(response1.status_code, 200)
        body1 = json.loads(str(response1.data, "utf8"))
        self.assertDictEqual(body1, {"microservice": "resource gathering"})

        response2 = self.app.get("http://127.0.0.1:5000/") #CachingService
        self.assertEqual(response2.status_code, 200)
        body2 = json.loads(str(response1.data, "utf8"))
        self.assertDictEqual(body2, {"microservice": "Caching Server"})

        response3 = self.app.get("http://127.0.0.1:9000/") #AuthenticationService
        self.assertEqual(response3.status_code, 200)
        body3 = json.loads(str(response1.data, "utf8"))
        self.assertDictEqual(body3, {"microservice": "Authentication Server"})

        response4 = self.app.get("http://127.0.0.1:7000/") #Jamdo App
        self.assertEqual(response4.status_code, 200) #Can't test html
        
       