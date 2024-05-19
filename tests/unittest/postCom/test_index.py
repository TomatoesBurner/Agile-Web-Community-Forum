import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel
from config import TestConfig

class TestIndex(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试用户
        self.test_user = UserModel(email='test@example.com', username='testuser', security_question='Test question',avatar='default_avatar.png')
        self.test_user.set_password('password')
        self.test_user.set_security_answer('answer')
        db.session.add(self.test_user)
        db.session.commit()

        # 登录用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

        # 创建测试帖子
        self.test_post = PostModel(
            title='Test Post',
            content='This is a test post.',
            post_type='G',
            author_id=self.test_user.id,
            postcode=1234
        )
        db.session.add(self.test_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.client.get(url_for('postCom.index'))
        response_text = response.data.decode()
        print(response_text)  # 打印响应内容以诊断问题
        self.assertEqual(response.status_code, 200)
        # 根据实际内容修改断言，假设帖子标题为 'Test Post'
        self.assertIn(b'Test Post', response_text)

if __name__ == '__main__':
    unittest.main()
