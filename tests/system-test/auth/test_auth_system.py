import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app
from config import TestConfig
from multiprocessing import Process, set_start_method
import time
from app.extensions import db
import os

set_start_method('spawn', force=True)

# 确保在测试环境中没有 DATABASE_URL 环境变量
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

# 打印当前所有环境变量以确保 DATABASE_URL 已被删除
for key, value in os.environ.items():
    print(f'{key}: {value}')


def start_flask_app():
    app = create_app(TestConfig)
    app.run(port=5001)


class SeleniumTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        print("Database URI in setUpClass: ", cls.app.config['SQLALCHEMY_DATABASE_URI'])

        with cls.app.app_context():
            db.create_all()

        cls.server_process = Process(target=start_flask_app)
        cls.server_process.start()
        time.sleep(1)

        chrome_options = ChromeOptions()
        chrome_options.headless = True
        cls.chrome_driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.chrome_driver.quit()
        cls.server_process.terminate()

        with cls.app.app_context():
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

        cls.app_context.pop()

    def setUp(self):
        with self.app.app_context():
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def test_register(self):
        self.chrome_driver.get('http://127.0.0.1:5001/register')

        WebDriverWait(self.chrome_driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )

        self.chrome_driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.chrome_driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.chrome_driver.find_element(By.NAME, 'password').send_keys('password123')
        self.chrome_driver.find_element(By.NAME, 'password_confirm').send_keys('password123')
        self.chrome_driver.find_element(By.NAME, 'security_question').send_keys('What is your pet\'s name?')
        self.chrome_driver.find_element(By.NAME, 'security_answer').send_keys('Fluffy')

        WebDriverWait(self.chrome_driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'register'))
        )

        self.chrome_driver.find_element(By.NAME, 'register').click()

        WebDriverWait(self.chrome_driver, 10).until(
            EC.title_contains('Login')
        )
        self.assertIn('Congratulations, you are now a registered user!', self.chrome_driver.page_source)


if __name__ == '__main__':
    unittest.main()
