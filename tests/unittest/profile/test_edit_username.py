import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel
from config import TestConfig

class TestEditUsername(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试用户
        self.test_user = UserModel(
            email='test@example.com',
            username='testuser',
            avatar='images/default_avatar.png',  # 设置默认头像路径
            security_question='Test question'
        )
        self.test_user.set_password('password')
        self.test_user.set_security_answer('answer')
        db.session.add(self.test_user)
        db.session.commit()

        # 登录测试用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_edit_username(self):
        response = self.client.post(url_for('profile.edit_username'), data={
            'username': 'newtestuser'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'newtestuser', response.data)
        user = UserModel.query.get(self.test_user.id)
        self.assertEqual(user.username, 'newtestuser')

if __name__ == '__main__':
    unittest.main()
