import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel
from config import TestConfig

class TestSecurityQuestion(unittest.TestCase):

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

    def test_valid_security_answer(self):
        response = self.client.post(url_for('auth.security_question', email='test@example.com'), data={
            'security_answer': 'answer',
            'new_password': 'new_password',
            'confirm_password': 'new_password',
            'submit': 'Reset Password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  #
        self.assertIn(b'Your password has been reset!', response.data)  #
        user = UserModel.query.filter_by(email='test@example.com').first()
        self.assertTrue(user.check_password('new_password'))

    def test_invalid_security_answer(self):
        response = self.client.post(url_for('auth.security_question', email='test@example.com'), data={
            'security_answer': 'wrong_answer',
            'new_password': 'new_password',
            'confirm_password': 'new_password',
            'submit': 'Reset Password'
        })
        print(response.data.decode())  #
        self.assertEqual(response.status_code, 200)  #
        self.assertIn(b'Incorrect answer to the security question', response.data)  #
    def test_password_mismatch(self):
        response = self.client.post(url_for('auth.security_question', email='test@example.com'), data={
            'security_answer': 'answer',
            'new_password': 'new_password1',
            'confirm_password': 'new_password2',
            'submit': 'Reset Password'
        })
        response_text = response.data.decode()
        print(response_text)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Passwords must match', response_text)

    def test_invalid_email(self):
        response = self.client.get(url_for('auth.security_question', email='invalid@example.com'))
        self.assertEqual(response.status_code, 302)  # redirect forgot_password page


if __name__ == '__main__':
    unittest.main()
