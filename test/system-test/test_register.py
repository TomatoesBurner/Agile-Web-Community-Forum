import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app import create_app, db

class SystemRegisterTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(config_class='test_config.TestConfig')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

    # 设置webdriver
    self.driver = webdriver.Chrome()
    self.driver.implicitly_wait(10)
    self.base_url = 'http://localhost:5000'

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
    self.driver.quit()

  def test_register(self):
    driver = self.driver
    driver.get(self.base_url + '/register')

    # 填写注册表单
    driver.find_element(By.NAME, 'email').send_keys('test@example.com')
    driver.find_element(By.NAME, 'username').send_keys('testuser')
    driver.find_element(By.NAME, 'password').send_keys('testpassword')
    driver.find_element(By.NAME, 'password2').send_keys('testpassword')
    driver.find_element(By.NAME, ' submit').click()

    # 检查是否注册成功
    self.assertIn('Congratulations', driver.page_souce)

if __name__ == '__main__':
  unittest.main()