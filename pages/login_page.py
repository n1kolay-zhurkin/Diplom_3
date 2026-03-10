import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Войти')]")

    @allure.step("Вход в систему")
    def login(self, email, password):
        print(f"\n=== Заполнение формы входа ===")
        print(f"Email: {email}")
        print(f"Пароль: {password}")

        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

        # Ждем возвращения на главную страницу
        self.wait.until(EC.url_to_be("https://stellarburgers.education-services.ru/"))
        print("✓ Успешный вход в систему")