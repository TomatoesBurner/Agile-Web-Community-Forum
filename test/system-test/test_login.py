import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app import create_app, db
from app.models import UserModel

class SystemLoginTestCase(unittest.TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def test_login(self):
        driver = self.driver
        driver.get(self.base_url + '/login')

        # 填写登录表单
        driver.find_element(By.NAME, 'email').send_keys('test@example.com')
        driver.find_element(By.NAME, 'password').send_keys('testpassword')
        driver.find_element(By.NAME, 'submit').click()

        # 检查是否成功登录
        self.assertIn('Index', driver.page_source)  # 假设主页包含 'Index'
        self.assertNotIn('Login', driver.page_source)  # 确保不在登录页面

if __name__ == '__main__':
    unittest.main()
