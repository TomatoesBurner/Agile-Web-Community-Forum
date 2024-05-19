import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel, CommentModel
from config import TestConfig
from flask_login import current_user


class TestAcceptComment(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试用户和帖子
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

        self.other_user = UserModel(
            email='other@example.com',
            username='otheruser',
            avatar='images/default_avatar.png',  # 设置默认头像路径
            security_question='Test question'
        )
        self.other_user.set_password('password')
        self.other_user.set_security_answer('answer')
        db.session.add(self.other_user)
        db.session.commit()

        # 登录测试用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

        # 创建测试帖子和评论
        self.test_post = PostModel(
            title='Test Post',
            content='This is a test post.',
            post_type='G',
            author_id=self.test_user.id,
            postcode=1234
        )
        db.session.add(self.test_post)
        db.session.commit()

        self.test_comment = CommentModel(
            content='This is a test comment.',
            post_id=self.test_post.id,
            author_id=self.other_user.id
        )
        db.session.add(self.test_comment)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_accept_comment_as_author(self):
        # 测试作为作者采纳评论
        response = self.client.post(
            url_for('postCom.accept_comment', post_id=self.test_post.id, comment_id=self.test_comment.id),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)
        self.assertIn(b'This is a test comment.', response.data)

        # 检查评论是否被采纳
        comment = CommentModel.query.get(self.test_comment.id)
        self.assertTrue(comment.is_accepted)
        post = PostModel.query.get(self.test_post.id)
        self.assertEqual(post.accepted_answer_id, self.test_comment.id)

    def test_accept_comment_as_non_author(self):
        # 以其他用户登录
        self.client.post(url_for('auth.logout'))
        self.client.post(url_for('auth.login'), data={
            'email': 'other@example.com',
            'password': 'password'
        })


