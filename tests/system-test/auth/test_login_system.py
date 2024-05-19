import unittest
import multiprocessing
import os
import time
from sqlalchemy import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from app import create_app, db
from config import SeleniumTestingConfig


def run_app():
    app = create_app(SeleniumTestingConfig)
    app.run(host='127.0.0.1', port=5001)  # 使用端口 5001


class AuthSystemTests(unittest.TestCase):

    def setUp(self):
        # 创建并配置 Flask 应用程序
        self.app = create_app(SeleniumTestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # 确保创建所有表

        # 打印已创建的表名
        with self.app.app_context():
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print("Created tables:", tables)

        # 启动 Flask 应用程序服务器
        self.server_process = multiprocessing.Process(target=run_app)
        self.server_process.start()
        time.sleep(2)  # 给服务器一些时间来启动

        # 自动检测系统中安装的浏览器并选择相应的 WebDriver
        browser = os.getenv('TEST_BROWSER', 'chrome')

        if browser == "chrome":
            # options = webdriver.ChromeOptions()
            # options.add_argument("--headless=new")
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        elif browser == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        else:
            raise ValueError("No supported browser found on the system!")

        self.driver.get("http://127.0.0.1:5001")  # 使用端口 5001

    def tearDown(self):
        # 清理数据库中的数据
        db.session.remove()

        # 手动删除表，确保删除顺序正确
        with self.app.app_context():
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 0;')
            db.engine.execute('DROP TABLE IF EXISTS notifications;')
            db.engine.execute('DROP TABLE IF EXISTS comments;')
            db.engine.execute('DROP TABLE IF EXISTS posts;')
            db.engine.execute('DROP TABLE IF EXISTS users;')
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 1;')

        db.drop_all()
        self.app_context.pop()

        # 关闭 WebDriver 并终止服务器
        self.driver.quit()
        self.server_process.terminate()
        self.server_process.join()

    def test_register_login(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)  # 设置显式等待时间为5秒

        with self.app.app_context():
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print("Created tables during test:", tables)

        # 导航到首页
        driver.get("http://127.0.0.1:5001/")  # 确保导航到正确的首页
        print("Navigating to Register page")
        try:
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register!"))).click()
            print("Register link clicked")
            with self.app.app_context():
                tables = inspect(db.engine).get_table_names()
                print("Tables after clicking register:", tables)
        except Exception as e:
            print("Failed to click Register link")
            print(e)
            self.fail("Register link not found or not clickable")

        try:
            wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("testuser2")
            wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("test2@example.com")
            wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("123456")
            wait.until(EC.presence_of_element_located((By.NAME, "password_confirm"))).send_keys("123456")
            wait.until(EC.presence_of_element_located((By.NAME, "security_question"))).send_keys("Test question")
            wait.until(EC.presence_of_element_located((By.NAME, "security_answer"))).send_keys("Test answer")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Register']"))).click()
            print("Registration form submitted")
            with self.app.app_context():
                tables = inspect(db.engine).get_table_names()
                print("Tables after submitting registration:", tables)
        except Exception as e:
            print("Failed to fill or submit registration form")
            print(e)
            self.fail("Failed to fill or submit registration form")

        # 登录用户
        try:
            wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("test2@example.com")
            wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("123456")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))).click()
            print("Login form submitted")
            with self.app.app_context():
                tables = inspect(db.engine).get_table_names()
                print("Tables after submitting login:", tables)
        except Exception as e:
            print("Failed to fill or submit login form")
            print(e)
            self.fail("Failed to fill or submit login form")

        # 断言登录成功
        try:
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
            self.assertIn("Logout", driver.page_source)
            print("Logout link found, login successful")
        except Exception as e:
            print("Logout link not found, login failed")
            print(e)
            self.fail("Logout link not found, login failed")


if __name__ == "__main__":
    unittest.main()