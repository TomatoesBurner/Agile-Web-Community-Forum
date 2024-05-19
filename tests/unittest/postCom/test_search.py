import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel
from config import TestConfig

class TestSearch(unittest.TestCase):

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

        # 创建测试帖子
        self.test_post1 = PostModel(
            title='Gardening Tips',
            content='This is a post about gardening.',
            post_type='G',
            author_id=self.test_user.id,
            postcode=1234
        )
        self.test_post2 = PostModel(
            title='Housing Work',
            content='This is a post about housing work.',
            post_type='HW',
            author_id=self.test_user.id,
            postcode=5678
        )
        db.session.add(self.test_post1)
        db.session.add(self.test_post2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_title(self):
        response = self.client.get(url_for('postCom.search', query='Gardening', scope='title'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gardening Tips', response.data)
        self.assertNotIn(b'Housing Work', response.data)

    def test_search_by_content(self):
        response = self.client.get(url_for('postCom.search', query='housing work', scope='content'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Housing Work', response.data)
        self.assertNotIn(b'Gardening Tips', response.data)

    def test_search_by_postcode(self):
        response = self.client.get(url_for('postCom.search', query='5678', scope='postcode'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'5678', response.data)

    def test_search_by_postcode_norightcode(self):
        response = self.client.get(url_for('postCom.search', query='1234', scope='postcode'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'5678', response.data)


    def test_search_by_all(self):
        response = self.client.get(url_for('postCom.search', query='gardening'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gardening Tips', response.data)
        self.assertNotIn(b'Housing Work', response.data)

    def test_search_empty_query(self):
        response = self.client.get(url_for('postCom.search', query=''))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gardening Tips', response.data)
        self.assertIn(b'Housing Work', response.data)

if __name__ == '__main__':
    unittest.main()
