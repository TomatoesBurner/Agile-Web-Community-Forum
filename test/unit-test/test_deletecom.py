import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel, CommentModel

class DeleteCommentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='test_config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # 创建一个测试用户
        self.user = UserModel(email='user@example.com', username='user')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

        # 使用 user 创建一个测试帖子
        self.client.post('/login', data={
            'email': 'user@example.com',
            'password': 'password'
        })
        self.client.post('/posts/create', data={
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_type': 'general'
        })

        # 获取创建的帖子
        self.post = PostModel.query.filter_by(title='Test Post').first()

        # 使用 user 创建一个测试评论
        self.client.post('/comments/create', data={
            'content': 'This is a test comment.',
            'post_id': self.post.id
        })

        # 获取创建的评论
        self.comment = CommentModel.query.filter_by(content='This is a test comment.').first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_delete_comment(self):
        """测试成功删除评论"""
        # 登录 user
        self.client.post('/login', data={
            'email': 'user@example.com',
            'password': 'password'
        })

        # 发送删除评论请求
        response = self.client.post(url_for('profile.delete_comment', comment_id=self.comment.id))
        self.assertEqual(response.status_code, 302)  # 成功后应重定向

        # 验证评论已被删除
        deleted_comment = CommentModel.query.get(self.comment.id)
        self.assertIsNone(deleted_comment)

if __name__ == '__main__':
    unittest.main()
