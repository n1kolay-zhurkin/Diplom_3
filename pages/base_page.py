import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Поиск видимого элемента: {locator}")
    def find_element(self, locator):
        """Найти видимый элемент с ожиданием"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Поиск всех видимых элементов: {locator}")
    def find_elements(self, locator):
        """Найти все видимые элементы с ожиданием"""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        """Клик по элементу"""
        self.find_element(locator).click()

    @allure.step("Ввод текста '{text}' в поле: {locator}")
    def send_keys(self, locator, text):
        """Ввод текста в поле"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return element

    @allure.step("Ожидание, что URL содержит '{text}'")
    def wait_for_url_contains(self, text):
        """Ожидание, что URL содержит указанный текст"""
        self.wait.until(EC.url_contains(text))

    @allure.step("Ожидание URL: {url}")
    def wait_for_url_to_be(self, url):
        """Ожидание конкретного URL"""
        self.wait.until(EC.url_to_be(url))

    @allure.step("Проверка наличия элемента: {locator}")
    def is_element_present(self, locator):
        """Проверяет наличие элемента на странице"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    @allure.step("Скролл к элементу")
    def scroll_to_element(self, element):
        """Скролл к элементу - принимает WebElement, не локатор"""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Возвращает текущий URL страницы"""
        return self.driver.current_url

    @allure.step("Нажать клавишу ESC")
    def press_escape(self):
        """Нажимает клавишу ESC на странице"""
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)