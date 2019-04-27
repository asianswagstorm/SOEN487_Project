import unittest
import json
import sqlite3
from routes import *
from config import TestConfig
from models import User, db
from main import app as tested_app 

tested_app.config.from_object(TestConfig)

class TestApp(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = tested_app.test_client()
        self.main = tested_app.app_context()
        with tested_app.app_context():
            db.init_app(tested_app)  # removes cyclic dependency??
        self.db.create_all()
        self.db.session.add(User(id=1, fname="Alice",lname= "Jackson", uname= "Alice_J", password="password"))
        self.db.session.add(User(id=2, fname="Bob",lname= "Builder", uname= "Bob_The_Builder", password="password"))

        try:
         self.db.session.commit()
        except:
         self.db.session.rollback()  
        finally:
         self.db.session.close() 
         self.app = tested_app.test_client()   

    @classmethod
    def tearDownClass(self): #tearDown After each test method tearDownClass
     
     # clean up the DB after the tests
     with tested_app.app_context():
      User.query.delete() #This gives an error Doesn't WORK
      self.db.session.commit()
      self.db.session.close()    

    
    def test_login_no_data(self):
        response = self.app.post("/login", data= {"username" : "" , "password" : ""})
        self.assertEqual(response.status_code, 422)

    def test_login_user_pass(self):
        response = self.app.post("/login", data= {"username" : "Alice_J" , "password" : "password"})
        self.assertEqual(response.status_code, 200)
        
    def test_login_user_incorrect_password(self):
        response = self.app.post("/login", data= {"username" : "Bob_The_Builder" , "password" : "hahahhaha"})
        self.assertEqual(response.status_code, 401)

    def test_login_username_not_exist(self):
        response = self.app.post("/login", data= {"username" : "Random_Guy123" , "password" : "hahahhaha"})
        self.assertEqual(response.status_code, 404)   

    def test_register_username_already_exist(self):
        response = self.app.post("/register", data= {"fname": "Alice" , "lname": "Jackson" ,"username" : "Alice_J" , "password" : "hahahhaha"})
        self.assertEqual(response.status_code, 500)   

    def test_register_no_data(self):
        response = self.app.post("/login", data= {"username" : "" , "password" : ""})
        self.assertEqual(response.status_code, 422)

    def test_register_pass(self):
        response = self.app.post("/register", data= {"fname": "Jackie" , "lname": "Chan" ,"username" : "JackieChan" , "password" : "password"})
        self.assertEqual(response.status_code, 200)       

    def test_logout(self):
        response = self.app.get("/logout")
        self.assertEqual(response.status_code, 200)         
    
if __name__ == '__main__':
    unittest.main()

    