import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app import create_app, db
from app.models import UserModel

class SystemPostTestCase(unittest.TestCase):
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

    def test_create_post(self):
        driver = self.driver
        driver.get(self.base_url + '/posts/create')

        # 填写发帖表单
        driver.find_element(By.NAME, 'title').send_keys('Test Post')
        driver.find_element(By.NAME, 'content').send_keys('This is a test post.')
        driver.find_element(By.NAME, 'submit').click()

        # 检查是否成功发帖
        self.assertIn('Test Post', driver.page_source)
        self.assertIn('This is a test post.', driver.page_source)

if __name__ == '__main__':
    unittest.main()
