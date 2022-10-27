import time

import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.common.by import By

from ui.fixtures import get_driver
from ui.pages.base_page import BasePage


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.login_page = LoginPage(driver)
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            self.main_page = MainPage(driver)


@pytest.fixture(scope='session')
def credentials():
    with open('/Users/konstantin.ermakov/Documents/creds', 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()

    return user, password


@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = get_driver(config['browser'])
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.login(*credentials)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


class LoginPage(BasePage):
    url = 'https://education.vk.company/'

    def login(self, user, password):
        self.click((By.XPATH, '/html/body/header/div/nav/button'))
        self.find((By.NAME, 'login')).send_keys(user)
        self.find((By.NAME, 'password')).send_keys(password)

        self.click((By.XPATH, '//html/body/div[4]/div/div[1]/form/button'))

        time.sleep(5)
        return MainPage(self.driver)


class MainPage(BasePage):
    url = 'https://education.vk.company/feed/'


class TestLogin(BaseCase):
    authorize = False

    @pytest.mark.skip("SKIP")
    def test_login(self, credentials):
        login_page = LoginPage(self.driver)
        login_page.login(*credentials)

        time.sleep(5)


class TestLK(BaseCase):

    def test_lk1(self):
        time.sleep(3)

    def test_lk2(self):
        time.sleep(3)
