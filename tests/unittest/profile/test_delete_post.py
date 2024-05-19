import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel, CommentModel, Notification
from config import TestConfig


class TestDeletePost(unittest.TestCase):

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

        self.test_notification = Notification(
            name='new_comment',
            user_id=self.test_user.id,
            post_id=self.test_post.id,
            payload_json='{"message": "Test notification"}'
        )
        db.session.add(self.test_notification)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_delete_post_as_author(self):
        # 登录测试用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

        response = self.client.post(url_for('profile.delete_post', post_id=self.test_post.id), follow_redirects=True)
        print(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        post = PostModel.query.get(self.test_post.id)
        self.assertIsNone(post)

        # 检查评论和通知是否被删除
        comment = CommentModel.query.filter_by(post_id=self.test_post.id).first()
        self.assertIsNone(comment)
        notification = Notification.query.filter_by(post_id=self.test_post.id).first()
        self.assertIsNone(notification)

    def test_delete_post_as_non_author(self):
        # 登录其他用户
        self.client.post(url_for('auth.logout'))
        self.client.post(url_for('auth.login'), data={
            'email': 'other@example.com',
            'password': 'password'
        })

        response = self.client.post(url_for('profile.delete_post', post_id=self.test_post.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        post = PostModel.query.get(self.test_post.id)
        self.assertIsNotNone(post)

    def test_delete_post_not_logged_in(self):
        self.client.post(url_for('auth.logout'))
        response = self.client.post(url_for('profile.delete_post', post_id=self.test_post.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)
        post = PostModel.query.get(self.test_post.id)
        self.assertIsNotNone(post)


if __name__ == '__main__':
    unittest.main()
