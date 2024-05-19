import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, Notification
from config import TestConfig
from datetime import datetime

class TestNotifications(unittest.TestCase):

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
            avatar='default_avatar.png',  # 设置默认头像路径
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

        # 创建测试通知
        self.test_notification = Notification(
            name='new_comment',
            user_id=self.test_user.id,
            post_id=1,
            timestamp=datetime.utcnow(),
            payload_json='{"message": "Test notification message"}'
        )
        db.session.add(self.test_notification)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_inbox(self):
        # 登录测试用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

        response = self.client.get(url_for('notify.inbox'))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('notifications', data)
        self.assertEqual(len(data['notifications']), 1)
        self.assertEqual(data['notifications'][0]['message'], 'Test notification message')

    def test_inbox_not_logged_in(self):
        response = self.client.get(url_for('notify.inbox'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_delete_all_notifications(self):
        # 登录测试用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

        response = self.client.post(url_for('notify.delete_all_notifications'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'All notifications deleted')
        notifications = Notification.query.filter_by(user_id=self.test_user.id).all()
        self.assertEqual(len(notifications), 0)

    def test_delete_all_notifications_not_logged_in(self):
        response = self.client.post(url_for('notify.delete_all_notifications'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)

if __name__ == '__main__':
    unittest.main()
