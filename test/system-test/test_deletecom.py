import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app import create_app, db
from app.models import UserModel, PostModel, CommentModel

class SystemDeleteCommentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='test_config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建一个测试用户
        self.user = UserModel(email='user@example.com', username='user')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

        # 创建一个测试帖子
        self.post = PostModel(title='Test Post', content='This is a test post.', post_type='general', author_id=self.user.id)
        db.session.add(self.post)
        db.session.commit()

        # 创建一个测试评论
        self.comment = CommentModel(content='This is a test comment.', post_id=self.post.id, author_id=self.user.id)
        db.session.add(self.comment)
        db.session.commit()

        # 设置 WebDriver
        self.driver = webdriver.Chrome()  # 确保已安装 ChromeDriver
        self.driver.implicitly_wait(10)
        self.base_url = 'http://localhost:5000'

        # 用户登录
        self.driver.get(self.base_url + '/login')
        self.driver.find_element(By.NAME, 'email').send_keys('user@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'submit').click()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def test_delete_comment(self):
        driver = self.driver
        driver.get(self.base_url + f'/delete_comment/{self.comment.id}')

        # 检查是否成功删除评论
        self.assertNotIn('This is a test comment.', driver.page_source)

if __name__ == '__main__':
    unittest.main()
