from unittest import TestCase, main

from app import app
from models import db, User, Post
from sqlalchemy.exc import IntegrityError

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

# this is part of the test below that I am trying to run but not having any luck with
# def raises_error():
#         print("raises_error was run")
#         raise IntegrityError


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""
    
    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="TestUser", last_name="test_last_name", image_url="http://placekitten.com/200/300")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.user_id
        
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)
            
    def test_list_users_links(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)
    
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser test_last_name', html)
            
    def test_fail_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/user/{self.user_id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 404)
        
    
    def test_add_user(self):
        with app.test_client() as client:
            user = {"first_name": "TestUser2", "last_name": "last_name_test", "image_url": "http://placekitten.com/g/200/300"}
            resp = client.post("/add", data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2 last_name_test", html)

    
# -------------------------------------------------------
    # Note trying to get this test to work. But having no luck will continue to try but continuing on for now. 
    
    # def test_fail_add_user(self):
    #     with app.test_client() as client:
    #         user = {"first_name": "TestUser", "last_name": "last_name", "image_url": "http://placekitten.com/g/200/300"}
    #         resp = client.post("/add", data=user, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
            
    #         self.assertRaises(IntegrityError, raises_error)
            
            
    # def test_fail_add_user(self):
    #     with app.test_client() as client:
    #         user = {"first_name": "TestUser", "last_name": "last_name", "image_url": "http://placekitten.com/g/200/300"}
    #         resp = client.post("/add", data=user, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #     with self.assertRaises(IntegrityError):
    #         raises_error()
            
    # def test_fail_add_user(self):
    #     with app.test_client() as client:
    #         user = {"first_name": "TestUser", "last_name": "last_name", "image_url": "http://placekitten.com/g/200/300"}
    #         resp = client.post("/add", data=user, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #         with self.assertRaises(IntegrityError):
    #             raises_error()
                
                
    # def test_fail_add_user(self):
    #     with app.test_client() as client:
    #         user = {"first_name": "TestUser", "last_name": "last_name", "image_url": "http://placekitten.com/g/200/300"}
    #         resp = client.post("/add", data=user, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #     with self.assertRaises(IntegrityError):
    #         raise IntegrityError
            
    # if __name__ == "__main__":
    #     main()
            
# -----------------------------------------------------------
            
    # still working on these will hopefully be able to figure them out but submitting for now. 
    # def test_post_edited_user(self):
    #     with app.test_client() as client:
    #         user = {"first_name": "TestUser", "last_name": "test_last_name", "image_url": "http://placekitten.com/200/300"}
    #         resp = client.post("/users", data=user, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("TestUser test_last_name", html)
            
    # def test_delete_user(self):
    #     with app.test_client() as client:
    #         user = {"first_name": "TestUser2", "last_name": "last_name_test", "image_url": "http://placekitten.com/g/200/300"}
            
        