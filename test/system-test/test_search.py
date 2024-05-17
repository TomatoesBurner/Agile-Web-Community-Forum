import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import create_app, db
from app.models import UserModel, PostModel

class SystemSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='test_config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

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

        # 设置 WebDriver
        self.driver = webdriver.Chrome()  # 确保已安装 ChromeDriver
        self.driver.implicitly_wait(10)
        self.base_url = 'http://localhost:5000'

        # 用户登录
        self.driver.get(self.base_url + '/login')
        self.driver.find_element(By.NAME, 'email').send_keys('test@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('testpassword')
        self.driver.find_element(By.NAME, 'submit').click()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def test_search_by_title(self):
        """根据标题搜索"""
        driver = self.driver
        driver.get(self.base_url + '/search?query=First&scope=title')
        self.assertIn('First Post', driver.page_source)
        self.assertNotIn('Second Post', driver.page_source)

    def test_search_by_content(self):
        """根据内容搜索"""
        driver = self.driver
        driver.get(self.base_url + '/search?query=second&scope=content')
        self.assertIn('Second Post', driver.page_source)
        self.assertNotIn('First Post', driver.page_source)

    def test_search_by_all(self):
        """根据标题和内容搜索"""
        driver = self.driver
        driver.get(self.base_url + '/search?query=Content')
        self.assertIn('First Post', driver.page_source)
        self.assertIn('Second Post', driver.page_source)

    def test_search_no_results(self):
        """测试搜索无果的结果"""
        driver = self.driver
        driver.get(self.base_url + '/search?query=Nonexistent')
        self.assertNotIn('First Post', driver.page_source)
        self.assertNotIn('Second Post', driver.page_source)
        self.assertIn('No posts found', driver.page_source)  # 假设模板中有这个提示

if __name__ == '__main__':
    unittest.main()
