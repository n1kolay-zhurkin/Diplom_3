import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.urls import Urls


class LoginPage(BasePage):
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Войти')]")

    @allure.step("Вход в систему с email: {email}")
    def login(self, email, password):
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_url_to_be(Urls.BASE)