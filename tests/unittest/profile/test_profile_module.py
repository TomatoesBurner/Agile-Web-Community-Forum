import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel, CommentModel, Notification
from config import TestConfig

class ProfileTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.test_user = UserModel(
            email='test@example.com',
            username='testuser',
            avatar='default_avatar.png',
            security_question='Test question'
        )
        self.test_user.set_password('password')
        self.test_user.set_security_answer('answer')
        db.session.add(self.test_user)
        db.session.commit()

        self.other_user = UserModel(
            email='other@example.com',
            username='otheruser',
            avatar='default_avatar.png',
            security_question='Test question'
        )
        self.other_user.set_password('password')
        self.other_user.set_security_answer('answer')
        db.session.add(self.other_user)
        db.session.commit()

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
            author_id=self.test_user.id
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

        # 登录测试用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_delete_comment_as_author(self):
        response = self.client.post(url_for('profile.delete_comment', comment_id=self.test_comment.id),
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        comment = db.session.get(CommentModel, self.test_comment.id)
        self.assertIsNone(comment)



    def test_delete_post_as_author(self):
        response = self.client.post(url_for('profile.delete_post', post_id=self.test_post.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        post = db.session.get(PostModel, self.test_post.id)
        self.assertIsNone(post)

        comment = CommentModel.query.filter_by(post_id=self.test_post.id).first()
        self.assertIsNone(comment)
        notification = Notification.query.filter_by(post_id=self.test_post.id).first()
        self.assertIsNone(notification)

    def test_edit_username(self):
        response = self.client.post(url_for('profile.edit_username'), data={
            'username': 'newtestuser'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'newtestuser', response.data)
        user = db.session.get(UserModel, self.test_user.id)
        self.assertEqual(user.username, 'newtestuser')

    def test_overview_profile(self):
        response = self.client.get(url_for('profile.overview_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)
        self.assertIn(b'Test Post', response.data)
        self.assertIn(b'This is a test comment.', response.data)


if __name__ == '__main__':
    unittest.main()
