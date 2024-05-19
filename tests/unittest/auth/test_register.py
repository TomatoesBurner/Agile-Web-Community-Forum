# tests/unittest/auth/test_register.py
import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel
from config import TestConfig

class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        response = self.client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password',
            'password_confirm': 'password',
            'security_question': 'New question',
            'security_answer': 'new_answer',
            'submit': 'Register'
        })
        self.assertEqual(response.status_code, 302)
        user = UserModel.query.filter_by(email='newuser@example.com').first()
        self.assertIsNotNone(user)

    def test_already_logged_in_user(self):
        user = UserModel(email='test@example.com', username='testuser', security_question='Test question')
        user.set_password('password')
        user.set_security_answer('answer')
        db.session.add(user)
        db.session.commit()

        with self.client:
            self.client.post(url_for('auth.login'), data={
                'email': 'test@example.com',
                'password': 'password',
                'submit': 'Sign In'
            })
            response = self.client.get(url_for('auth.register'))
            self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
