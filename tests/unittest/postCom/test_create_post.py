import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel
from config import TestConfig

class TestCreatePost(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试用户
        self.test_user = UserModel(email='test@example.com', username='testuser', security_question='Test question', avatar='default_avatar.png')
        self.test_user.set_password('password')
        self.test_user.set_security_answer('answer')
        db.session.add(self.test_user)
        db.session.commit()

        # 登录用户
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        response = self.client.post(url_for('postCom.create_post'), data={
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_type': 'G',
            'postcode': '1234'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'Test Post', response.data)

    def test_create_post_missing_postcode(self):
        response = self.client.post(url_for('postCom.create_post'), data={
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_type': 'G'
            # postcode is missing
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'missing postcode!', response.data)  # Assuming the error message is "missing postcode!"

    def test_create_post_missing_post_type(self):
        response = self.client.post(url_for('postCom.create_post'), data={
            'title': 'Test Post',
            'content': 'This is a test post.',
            'postcode': '1234'
            # post_type is missing
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'please select type', response.data)  # Assuming the error message is "please select type"

    def test_create_post_invalid_postcode_length(self):
        response = self.client.post(url_for('postCom.create_post'), data={
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_type': 'G',
            'postcode': '12345'  # Invalid postcode, more than 4 digits
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be between 1 and 4 characters long.', response.data)  # Assuming this error message

    def test_create_post_invalid_type(self):
        response = self.client.post(url_for('postCom.create_post'), data={
            'title': 'Test Post',
            'content': 'This is a test post.',
            'post_type': 'A',
            'postcode': '1234'  # Invalid postcode, more than 4 digits
        }, follow_redirects=True)
        print(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Not a valid choice.', response.data)

    def test_create_post_content_too_long(self):
        long_content = 'A' * 1001  # Content with 1001 characters
        response = self.client.post(url_for('postCom.create_post'), data={
            'title': 'Test Post',
            'content': long_content,
            'post_type': 'G',
            'postcode': '1234'
        }, follow_redirects=True)
        # print(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_create_post_title_too_long(self):
        long_content = 'A' * 201  # Content with 1001 characters
        response = self.client.post(url_for('postCom.create_post'), data={
            'title': 'Test Post',
            'content': long_content,
            'post_type': 'G',
            'postcode': '1234'
        }, follow_redirects=True)
        # print(response.data.decode())
        self.assertEqual(response.status_code, 200)


