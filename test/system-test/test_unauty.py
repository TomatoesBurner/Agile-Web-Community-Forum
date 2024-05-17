import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app import create_app, db

class SystemUnauthenticatedAccessTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class='test_config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 设置 WebDriver
        self.driver = webdriver.Chrome()  # 确保已安装 ChromeDriver
        self.driver.implicitly_wait(10)
        self.base_url = 'http://localhost:5000'

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def test_unauthenticated_access(self):
        """测试未登录用户访问受保护页面的行为"""
        driver = self.driver
        urls = [
            self.base_url + '/index',  # Example of an index page for posts
            self.base_url + '/posts/1',  # Example of a view post page
            self.base_url + '/register',  # Register page (if it's protected)
            self.base_url + '/logout',  # Logout page
            self.base_url + '/profile'  # Profile overview
        ]

        for url in urls:
            driver.get(url)
            self.assertIn('/login', driver.current_url)

        # Test access to login page
        driver.get(self.base_url + '/login')
        self.assertIn('Login', driver.page_source)

if __name__ == '__main__':
    unittest.main()
