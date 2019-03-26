import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import db, User, Project, Files             

tested_app.config.from_object(TestConfig)

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()
        self.main = tested_app.app_context()
        with tested_app.app_context():
            db.init_app(tested_app)                                    # removes cyclic dependency??
            db.create_all()
            db.session.add(User(username="Alice", email='alice@mail.com', password='pass'))
            db.session.add(User(username="Bob", email='bob@mail.com', password='pass'))        
            db.session.commit()
        

    def tearDown(self):
        # clean up the DB after the tests
        with tested_app.app_context():
            User.query.delete()
            db.session.commit()

    def test_get_all_user(self):
        # send the request and check the response status code
        response = self.app.get("/api/users")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        resp_json = json.loads(str(response.data, "utf8"))
        user_list = resp_json['users']
        self.assertEqual(type(user_list), list)
        self.assertDictEqual(user_list[0], {"id": 1, "username": "Alice", 'email':'alice@mail.com'})
        self.assertDictEqual(user_list[1], {"id": 2, "username": "Bob",'email':'bob@mail.com'})

    def test_get_user_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/api/users/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        resp_json = json.loads(str(response.data, "utf8"))
        user = resp_json['users']
        self.assertDictEqual(user[0], {"id": 1, "username": "Alice", 'email':'alice@mail.com'})

    def test_get_user_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/api/users/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this user id."})

    def test_put_user_with_new_id(self):
        # send the request and check the response status code
        response = self.app.post("/signup", data=dict(
            username="Ash", 
            email='ash@mail.com', 
            password='pass'
            ))
        self.assertEqual(response.status_code, 200)

        # get all users JSON by API
        response = self.app.get("/api/users")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        resp_json = json.loads(str(response.data, "utf8"))
        user_list = resp_json['users']
        self.assertEqual(type(user_list), list)
        for user in user_list:
            if user['username'] == 'Ash':
                self.assertTrue()
                #self.assertDictEqual(user_list[0], {"id": 1, "username": "Ash", 'email':'ash@mail.com'})


if __name__ == '__main__':
    unittest.main()