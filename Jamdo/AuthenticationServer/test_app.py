import unittest
import json
from main import app as tested_app
from config import TestConfig
from routes import *

tested_app.config.from_object(TestConfig)

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()
        self.main = tested_app.app_context()
        with tested_app.app_context():
            db.init_app(tested_app)                                    # removes cyclic dependency??
            db.create_all()
            db.session.commit()

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_404_on_invalid_url(self):
        # send the request and check the response status code
        response = self.app.get("/something")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()