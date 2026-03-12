import allure
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class MainPage(BasePage):
    # Верхнее меню
    CONSTRUCTOR_LINK = (By.XPATH, "//a[.//p[text()='Конструктор']]")
    ORDER_FEED_LINK = (By.XPATH, "//a[.//p[text()='Лента Заказов']]")
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//a[.//p[text()='Личный кабинет']]")

    # Заголовок конструктора
    CONSTRUCTOR_HEADER = (By.XPATH, "//h1[contains(text(),'Соберите бургер')]")

    # Зона конструктора
    BURGER_CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor')]")

    # Кнопка оформления заказа
    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(),'Оформить заказ')]")

    # Модальное окно заказа
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal')]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal')]//h2[contains(@class, 'text_type_digits-large')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//div[contains(@class, 'Modal')]//button")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")

    # Альтернативный локатор для номера заказа
    ALT_ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")

    @staticmethod
    def ingredient_by_alt(alt_text):
        return (By.XPATH, f"//img[@alt='{alt_text}']")

    @staticmethod
    def ingredient_counter(alt_text):
        return (By.XPATH, f"//img[@alt='{alt_text}']/ancestor::*[contains(@class, 'BurgerIngredient')]//*[contains(@class, 'counter_counter__num')]")

    @allure.step("Клик по ссылке 'Личный кабинет'")
    def click_personal_account(self):
        self.click(self.PERSONAL_ACCOUNT_LINK)

    @allure.step("Клик по ссылке 'Конструктор'")
    def click_constructor(self):
        self.click(self.CONSTRUCTOR_LINK)
        self.wait.until(EC.visibility_of_element_located(self.CONSTRUCTOR_HEADER))

    @allure.step("Клик по ссылке 'Лента Заказов'")
    def click_order_feed(self):
        self.click(self.ORDER_FEED_LINK)
        self.wait_for_url_contains("/feed")

    @allure.step("Клик по ингредиенту: {alt_text}")
    def click_ingredient(self, alt_text):
        self.click(self.ingredient_by_alt(alt_text))

    @allure.step("Получить счётчик ингредиента: {alt_text}")
    def get_ingredient_counter(self, alt_text):
        locator = self.ingredient_counter(alt_text)
        if self.is_element_present(locator):
            return int(self.find_element(locator).text)
        return 0

    @allure.step("Добавить ингредиент в заказ: {alt_text}")
    def add_ingredient_to_order(self, alt_text):
        ingredient = self.find_element(self.ingredient_by_alt(alt_text))
        target = self.find_element(self.BURGER_CONSTRUCTOR_AREA)

        self.scroll_to_element(ingredient)
        # Небольшая пауза для стабилизации после скролла
        self.wait.until(EC.visibility_of(ingredient))

        before = self.get_ingredient_counter(alt_text)

        actions = ActionChains(self.driver)
        actions.click_and_hold(ingredient).move_to_element(target).release().perform()

        self.wait.until(lambda d: self.get_ingredient_counter(alt_text) > before)
        after = self.get_ingredient_counter(alt_text)
        return after

    @allure.step("Нажать кнопку 'Оформить заказ'")
    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.ORDER_MODAL))
        # Ждем появления номера в модальном окне
        self.wait.until(EC.visibility_of_element_located(self.ORDER_MODAL_NUMBER))

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        """Получает номер заказа из модального окна с ожиданием появления настоящего номера"""
        try:
            # Ждем, пока номер перестанет быть 9999 (максимум 10 секунд)
            self.wait.until(
                lambda driver: driver.find_element(*self.ORDER_MODAL_NUMBER).text != "9999"
            )
            number_element = self.find_element(self.ORDER_MODAL_NUMBER)
            number = number_element.text
            return number
        except Exception:
            # Если не дождались, пробуем альтернативный локатор
            try:
                number_element = self.find_element(self.ALT_ORDER_NUMBER)
                number = number_element.text
                return number
            except:
                return "9999"

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        """Закрывает модальное окно с номером заказа"""
        try:
            # Находим крестик
            close_button = self.find_element(self.CLOSE_MODAL_BUTTON)
            
            # Используем JavaScript для клика (обходит оверлей)
            self.driver.execute_script("arguments[0].click();", close_button)
            
            # Ждем закрытия модального окна
            self.wait.until(EC.invisibility_of_element_located(self.ORDER_MODAL))
            
        except Exception:
            # Если не получилось, пробуем клик по оверлею
            try:
                overlay = self.find_element(self.MODAL_OVERLAY)
                self.driver.execute_script("arguments[0].click();", overlay)
                self.wait.until(EC.invisibility_of_element_located(self.ORDER_MODAL))
            except Exception:
                # Если ничего не помогло, нажимаем ESC через метод BasePage
                self.press_escape()
                self.wait.until(EC.invisibility_of_element_located(self.ORDER_MODAL))