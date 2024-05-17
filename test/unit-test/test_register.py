import unittest
from flask import current_app
from flask_login import current_user
from app import create_app, db
from app.models import UserModel

class RegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='test_config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_successful_registration(self): # 成功注册
        response = self.client.post('/register', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # 重定向到登录页面
        user = UserModel.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)

    def test_duplicate_email_registration(self): # 重复邮箱注册
        user = UserModel(email='test@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/register', data={
            'email': 'test@example.com',
            'username': 'testuser2',
            'password': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # 返回注册页面
        self.assertIn(b'Email address already exists', response.data)

    def test_duplicate_username_registration(self): # 重复用户名注册
        user = UserModel(email='test2@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/register', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # 返回注册页面
        self.assertIn(b'Username already exists', response.data)

    def test_password_mismatch(self): # 密码不匹配
        response = self.client.post('/register', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)  # 返回注册页面
        self.assertIn(b'Passwords must match', response.data)

    def test_invalid_email_format(self): # 无效的邮箱格式
        response = self.client.post('/register', data={
            'email': 'invalid-email',
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # 返回注册页面
        self.assertIn(b'Invalid email address', response.data)

    def test_short_password(self): # 无效的密码长度
        response = self.client.post('/register', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'short',
            'password2': 'short'
        })
        self.assertEqual(response.status_code, 200)  # 返回注册页面
        self.assertIn(b'Field must be at least 6 characters long', response.data)

    def test_access_register_when_logged_in(self):
        # 注册并登录一个用户
        user = UserModel(email='test@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        # 尝试访问注册页面
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 302)  # 重定向到首页

if __name__ == '__main__':
    unittest.main()
