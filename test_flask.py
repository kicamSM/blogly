from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""
    
    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="TestUser", last_name="test_last_name", image_url="http://placekitten.com/200/300")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        
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
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser test_last_name', html)
    
    def test_add_user(self):
        with app.test_client() as client:
            user = {"first_name": "TestUser2", "last_name": "last_name_test", "image_url": "http://placekitten.com/g/200/300"}
            resp = client.post("/add", data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2 last_name_test", html)
            
            
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
            
        