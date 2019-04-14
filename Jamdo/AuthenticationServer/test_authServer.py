import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import db, Services

tested_app.config.from_object(TestConfig)

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()
        self.main = tested_app.app_context()
        with tested_app.app_context():
            db.create_all()
            db.init_app(tested_app)
            #remove previous registrations at startup
            Services.query.delete()
            
            # create server specific passwords
            application_server = Services.query.filter_by(service='application').first()
            app_pass = "THIS_IS_APPLICATION_SERVER_PASSWORD"
            application_server.password = app_pass            

            resource_server = Services.query.filter_by(service='resource').first()
            res_pass = "THIS_IS_RESOURCE_SERVER_PASSWORD"
            resource_server.password = res_pass

            cache_server = Services.query.filter_by(service='cacheing').first()
            cache_pass = "THIS_IS_CACHING_SERVER_PASSWORD"
            cache_server.password = cache_pass

            db.session.commit()
        

    def tearDown(self):
        # clean up the DB after the tests
        with tested_app.app_context():
            Services.query.delete()
            db.session.commit()

    # approved service, password
    # gets token, authenticates
    # also checks against DB?
    def test_get_token(self):
        # send the request and check the response status code
        response = self.app.get("/api/users")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        resp_json = json.loads(str(response.data, "utf8"))
        user_list = resp_json['users']
        self.assertEqual(type(user_list), list)
        self.assertDictEqual(user_list[0], {"id": 1, "username": "Alice", 'email':'alice@mail.com'})
        self.assertDictEqual(user_list[1], {"id": 2, "username": "Bob",'email':'bob@mail.com'})

    def test_get_token_invalid_service(self):
        # send the request and check the response status code
        response = self.app.get("/api/users/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        resp_json = json.loads(str(response.data, "utf8"))
        user = resp_json['users']
        self.assertDictEqual(user[0], {"id": 1, "username": "Alice", 'email':'alice@mail.com'})

    def test_get_token_invalid_password(self):
        # send the request and check the response status code
        response = self.app.get("/api/users/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this user id."})

    def test_authenticate(self):
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

    def test_authenticate_no_token(self):
        return

    def test_authenticate_invalid_token(self):
        return

    def test_authenticate_unrecognized_token(self):
        return

    """ 
    # never reaches these
    def test_authenticate_token_expired(self):
        return

    def test_authenticate_decode_invalid(self):
        return        
    """
if __name__ == '__main__':
    unittest.main()