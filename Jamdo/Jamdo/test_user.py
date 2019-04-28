import unittest
import json
import sqlite3
from routes import *
from config import TestConfig
from models import User, db as tested_db
from main import app as tested_app , bcrypt 

"""
from routes import *
from config import TestConfig
from main import app as tested_app
"""
tested_app.config.from_object(TestConfig)

class TestApp(unittest.TestCase):
    @classmethod
    def setUp(self):
       
        self.db = tested_db 
        self.db.create_all()
        self.db.session.add(User(id=1, fname="Alice",lname= "Jackson", username= "Alice_J", password=bcrypt.generate_password_hash("password")))
        self.db.session.add(User(id=2, fname="Bob",lname= "Builder", username= "Bob_The_Builder", password=bcrypt.generate_password_hash("password")))
        try:
         self.db.session.commit()
        except:
         self.db.session.rollback()  
        finally:
         self.db.session.close() 
         self.app = tested_app.test_client()   
         #self.main = tested_app.app_context()

    @classmethod
    def tearDownClass(self): #tearDown After each test method tearDownClass
       # clean up the DB after the tests
       User.query.delete() 
       self.db.session.commit() 
       self.db.session.close() 
      # pass
    
    #Problem with data input, unit test is not taking in data resulting in 422 error status
    def testA1_login_no_data(self):
        response = self.app.post("/login", data= {"username" : "" , "password" : ""})
        self.assertEqual(response.status_code, 422)

    def testA2_login_user_pass(self):
        response = self.app.post("/login", data= {"username" : "Alice_J" , "password" : "password"})
        self.assertEqual(response.status_code, 200)
        
    def testA3_login_user_incorrect_password(self):
        response = self.app.post("/login", data= {"username" : "Bob_The_Builder" , "password" : "hahahhaha"})
        self.assertEqual(response.status_code, 401)

    def testA4_login_username_not_exist(self):
        response = self.app.post("/login", data= {"username" : "Random_Guy123" , "password" : "hahahhaha"})
        self.assertEqual(response.status_code, 404)   
    
    def testA5_register_username_already_exist(self):
        response = self.app.post("/register", data= {"fname": "Alice" , "lname": "Jackson" ,"username" : "Alice_J" , "password" : "hahahhaha"})
        self.assertEqual(response.status_code, 500)   
    
    def testA6_register_no_data(self):
        response = self.app.post("/login", data= {"username" : "" , "password" : ""})
        self.assertEqual(response.status_code, 422)
    
    def testA7_register_pass(self):
        response = self.app.post("/register", data= {"fname": "Jackie" , "lname": "Chan" ,"username" : "JackieChan" , "password" : "password"})
        self.assertEqual(response.status_code, 200)       
    
    def test_logout(self): 
        response = self.app.get("/logout")
        self.assertEqual(response.status_code, 200)    

    def test_user_not_Admin(self): 
        response = self.app.get("/users")
        self.assertEqual(response.status_code, 401) 
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 401, "msg": "Protected Route only authorized accounts can access this route, Get out of here"})          
    
if __name__ == '__main__':
    unittest.main()

    