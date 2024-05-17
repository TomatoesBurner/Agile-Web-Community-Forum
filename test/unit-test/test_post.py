import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='test_config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # 注册并登录一个用户
        user = UserModel(email='test@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        # 测试发帖
        response = self.client.post('/posts/create', data={
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_type': 'general'
        })
        self.assertEqual(response.status_code, 302)  # 成功后应重定向

        # 验证帖子已创建
        post = PostModel.query.filter_by(title='Test Post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.author.username, 'testuser')

if __name__ == '__main__':
    unittest.main()
