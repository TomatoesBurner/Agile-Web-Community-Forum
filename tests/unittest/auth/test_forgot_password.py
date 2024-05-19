import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel
from config import TestConfig

class TestForgotPassword(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # create account
        self.test_user = UserModel(email='test@example.com', username='testuser', security_question='Test question')
        self.test_user.set_password('password')
        self.test_user.set_security_answer('answer')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_forgot_password(self):
        response = self.client.post(url_for('auth.forgot_password'), data={
            'email': 'test@example.com',
            'submit': 'Submit'
        })
        self.assertEqual(response.status_code, 302)
    def test_valid_email(self):
        response = self.client.post(url_for('auth.forgot_password'), data={
            'email': 'test@example.com',
            'submit': 'Submit'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Security Question', response.data)

if __name__ == '__main__':
    unittest.main()
