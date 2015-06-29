###### THIS FILE DOES NOT USE FOR THE PROJECT ######
###### It fails for this current project, but it all passes before when it's begining of this project.
#######################
####### imports #######
#######################
import unittest
from App import app, db
from flask.ext.testing import TestCase
from App.models import Users

class BasetestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Users("hanna", "hanna", "admin@test.com"))
        # db.session.add(BlogPost("hello", "hello"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class FlaskTestCase(BasetestCase):
    
    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEquals(response.status_code, 200)

    # Ensure that the login page loads correctly, to make sure that 
    # the right template is rendered, because return 200 cannot make sure that 
    # it returns the page we want, so include some content in the page just to make sure
    def test_login_page(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)
    
    
    # Ensure login behaves correctly given the correct credentials 
    def test_correct_login(self):
        response = self.client.post('/login', data=dict(user_name='hanna', user_password='hanna'), follow_redirects=True)
        self.assertIn(b'You are just login!', response.data)
        
        
    # Ensure login behaves correctly given the incorrect credentials 
    def test_incorrect_login(self):
        response = self.client.post('/login', data=dict(user_name='hello', user_password='hanna'), follow_redirects=True)
        self.assertIn(b'Invalid username or password. Please try again.', response.data)
        
     
    # Ensure logout behaves correctly
    def test_logout(self):
        self.client.post('/login', data=dict(user_name='hanna', user_password='hanna'), follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn('You are just logout!', response.data)
 
        
    # Ensure that the main page requires login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)
        
 
    # Ensure that the main page requires login
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)
 
    # Ensure that posts show up on the main page 
    # This is really not a good test, because we are testing data in the db
    # which can be removed any time
    def test_post_show_up(self):
        response = self.client.post('/login', data=dict(username='hanna', password='hanna'), follow_redirects=True)
        self.assertIn(b'Recipe', response.data)
    
if __name__ == '__main__':
    unittest.main()