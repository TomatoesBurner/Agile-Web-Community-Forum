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

    def test_valid_security_answer(self):
        response = self.client.post(url_for('auth.security_question', email='test@example.com'), data={
            'security_answer': 'answer',
            'new_password': 'new_password',
            'confirm_password': 'new_password',
            'submit': 'Reset Password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # 应该成功重定向到登录页面
        self.assertIn(b'Your password has been reset!', response.data)  # 检查成功消息
        user = UserModel.query.filter_by(email='test@example.com').first()
        self.assertTrue(user.check_password('new_password'))

    def test_invalid_security_answer(self):
        response = self.client.post(url_for('auth.security_question', email='test@example.com'), data={
            'security_answer': 'wrong_answer',
            'new_password': 'new_password',
            'confirm_password': 'new_password',
            'submit': 'Reset Password'
        })
        print(response.data.decode())  # 打印响应内容以诊断问题
        self.assertEqual(response.status_code, 200)  # 应该返回 security_question 页面
        self.assertIn(b'Incorrect answer to the security question', response.data)  # 检查错误消息
    def test_password_mismatch(self):
        response = self.client.post(url_for('auth.security_question', email='test@example.com'), data={
            'security_answer': 'answer',
            'new_password': 'new_password1',
            'confirm_password': 'new_password2',
            'submit': 'Reset Password'
        })
        response_text = response.data.decode()
        print(response_text)  # 打印响应内容以诊断问题
        self.assertEqual(response.status_code, 200)  # 应该返回 security_question 页面
        self.assertIn('Passwords must match', response_text)  # 检查错误消息

    def test_invalid_email(self):
        response = self.client.get(url_for('auth.security_question', email='invalid@example.com'))
        self.assertEqual(response.status_code, 302)  # 应该重定向到 forgot_password 页面
        self.assertIn(b'Invalid email address', response.data)  # 检查错误消息

if __name__ == '__main__':
    unittest.main()
