import unittest
from flask import url_for
from flask_login import current_user
from app import create_app, db
from app.models import UserModel
from config import TestConfig

class TestLogout(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.test_user = UserModel(email='test@example.com', username='testuser', security_question='Test question')
        self.test_user.set_password('password')
        self.test_user.set_security_answer('answer')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_logout(self):
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password',
            'submit': 'Sign In'
        })

        with self.client:
            self.client.get('/')
            self.assertTrue(current_user.is_authenticated)

            response = self.client.get(url_for('auth.logout'))
            self.assertEqual(response.status_code, 302)


            self.client.get('/')
            self.assertFalse(current_user.is_authenticated)

if __name__ == '__main__':
    unittest.main()
