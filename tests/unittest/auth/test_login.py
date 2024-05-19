import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel
from config import TestConfig


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试用户
        self.test_user = UserModel(email='test@example.com', username='testuser', security_question='Test question')
        self.test_user.set_password('password')
        self.test_user.set_security_answer('answer')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_valid_login(self):
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password',
            'submit': 'Sign In'
        })
        self.assertEqual(response.status_code, 302)  # 应该重定向到主页

    def test_invalid_login(self):
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'wrongpassword',
            'submit': 'Sign In'
        })
        self.assertEqual(response.status_code, 200)  # 应该返回登录页面
        self.assertIn(b'Invalid username or password', response.data)


if __name__ == '__main__':
    unittest.main()
