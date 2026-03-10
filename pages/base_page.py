from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BasePage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator):
        """Найти видимый элемент с ожиданием"""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"❌ Элемент не найден: {locator}")
            # Пробуем найти любой элемент с таким локатором для отладки
            elements = self.driver.find_elements(*locator)
            print(f"   Найдено элементов: {len(elements)}")
            raise

    def find_elements(self, locator):
        """Найти все видимые элементы с ожиданием"""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        """Клик по элементу"""
        self.find_element(locator).click()

    def send_keys(self, locator, text):
        """Ввод текста в поле с явным кликом и очисткой"""
        try:
            element = self.find_element(locator)
            element.click()
            time.sleep(0.3)
            element.clear()
            time.sleep(0.3)
            element.send_keys(text)
            time.sleep(0.3)
            print(f"   ✓ Текст '{text}' введен")
            return element
        except Exception as e:
            print(f"   ✗ Ошибка при вводе текста: {e}")
            raise

    def wait_for_url_contains(self, text):
        """Ожидание, что URL содержит указанный текст"""
        self.wait.until(EC.url_contains(text))

    def is_element_present(self, locator):
        """Проверяет наличие элемента на странице"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False