import unittest
from flask import url_for
from app import create_app, db
from app.models import UserModel, PostModel

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='test_config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # 创建一个测试用户
        user = UserModel(email='test@example.com', username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # 创建一些测试帖子
        post1 = PostModel(title='First Post', content='Content of the first post', post_type='general', author_id=user.id)
        post2 = PostModel(title='Second Post', content='Content of the second post', post_type='general', author_id=user.id)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_title(self): # 根据标题搜索
        response = self.client.get(url_for('postCom.search', query='First', scope='title'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'First Post', response.data)
        self.assertNotIn(b'Second Post', response.data)

    def test_search_by_content(self): # 根据内容搜索
        response = self.client.get(url_for('postCom.search', query='second', scope='content'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Second Post', response.data)
        self.assertNotIn(b'First Post', response.data)

    def test_search_by_all(self): # 根据标题和内容搜索
        response = self.client.get(url_for('postCom.search', query='Content'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'First Post', response.data)
        self.assertIn(b'Second Post', response.data)

    def test_search_no_results(self): # 测试搜索无果的结果
        response = self.client.get(url_for('postCom.search', query='Nonexistent'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'First Post', response.data)
        self.assertNotIn(b'Second Post', response.data)
        self.assertIn(b'No posts found', response.data)  # 假设模板中有这个提示

if __name__ == '__main__':
    unittest.main()
