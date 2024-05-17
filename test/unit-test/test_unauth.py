import unittest
from flask import url_for
from app import create_app, db

class UnauthenticatedAccessTestCase(unittest.TestCase):
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

    def test_unauthenticated_access(self):
        # 用于检查未登录用户访问受保护页面的行为
        urls = [
            url_for('postCom.index'),  # Example of an index page for posts
            url_for('postCom.post_detail', post_id=1),  # Example of a view post page
            url_for('auth.register'),  # Register page (if it's protected)
            url_for('auth.logout'),  # Logout page
            url_for('profile.overview_profile')  # Profile overview
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login', response.location)

        # Test access to login page
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()