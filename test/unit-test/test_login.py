import unittest
from flask import current_app
from flask_login import current_user
from app import create_app, db
from app.models import UserModel

class AuthTestCase(unittest.TestCase):
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

    def test_login(self):
        # 注册一个用户
        user = UserModel(email='test@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # 测试成功登录
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # 重定向到主页

        with self.client:
            self.client.get('/')
            self.assertTrue(current_user.is_authenticated)

    def test_login_invalid_password(self):
        # 注册一个用户
        user = UserModel(email='test@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # 测试使用错误的密码登录
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # 返回登录页面
        self.assertIn(b'Invalid username or password', response.data)

        with self.client:
            self.client.get('/')
            self.assertFalse(current_user.is_authenticated)

    def test_login_nonexistent_user(self):
        # 测试使用不存在的用户登录
        response = self.client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # 返回登录页面
        self.assertIn(b'Invalid username or password', response.data)

        with self.client:
            self.client.get('/')
            self.assertFalse(current_user.is_authenticated)

    def test_access_login_when_logged_in(self):
        # 注册并登录一个用户
        user = UserModel(email='test@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        # 尝试访问登录页面
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)  # 重定向到主页

if __name__ == '__main__':
    unittest.main()
