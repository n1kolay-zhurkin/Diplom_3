import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

class MainPage(BasePage):
    # Верхнее меню
    CONSTRUCTOR_LINK = (By.XPATH, "//a[.//p[text()='Конструктор']] | //a[contains(@href, 'constructor')]")
    ORDER_FEED_LINK = (By.XPATH, "//a[.//p[text()='Лента Заказов']] | //a[contains(@href, 'feed')]")
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//a[.//p[text()='Личный кабинет']] | //a[text()='Личный кабинет'] | //a[contains(@href, 'profile')]")

    # Зона конструктора
    BURGER_CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor')]")

    # Кнопка оформления заказа
    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(),'Оформить заказ')]")

    # Модальное окно заказа
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal')]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal')]//h2[contains(@class, 'text_type_digits-large')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//div[contains(@class, 'Modal')]//button")
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")

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
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Соберите бургер')]")))

    @allure.step("Клик по ссылке 'Лента Заказов'")
    def click_order_feed(self):
        self.click(self.ORDER_FEED_LINK)
        self.wait_for_url_contains("/feed")

    @allure.step("Клик по ингредиенту")
    def click_ingredient(self, alt_text):
        self.click(self.ingredient_by_alt(alt_text))

    @allure.step("Получить счётчик ингредиента")
    def get_ingredient_counter(self, alt_text):
        locator = self.ingredient_counter(alt_text)
        if self.is_element_present(locator):
            return int(self.find_element(locator).text)
        return 0

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self, alt_text):
        ingredient = self.find_element(self.ingredient_by_alt(alt_text))
        target = self.find_element(self.BURGER_CONSTRUCTOR_AREA)
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ingredient)
        time.sleep(1)
        
        before = self.get_ingredient_counter(alt_text)
        
        actions = ActionChains(self.driver)
        actions.click_and_hold(ingredient).move_to_element(target).release().perform()
        
        time.sleep(2)
        after = self.get_ingredient_counter(alt_text)
        print(f"   📊 Счётчик {alt_text}: {before} → {after}")
        return after

    @allure.step("Нажать кнопку 'Оформить заказ'")
    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.ORDER_MODAL))
        print("   ✓ Модальное окно открылось")
        time.sleep(1)

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        try:
            time.sleep(1)
            number_element = self.find_element(self.ORDER_MODAL_NUMBER)
            number = number_element.text
            print(f"   📋 Получен номер заказа: {number}")
            return number
        except Exception as e:
            alt_locator = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")
            number_element = self.find_element(alt_locator)
            number = number_element.text
            return number

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        print("\n   🗙 Закрытие модального окна...")
        time.sleep(1)
        
        # Способ 1: Клик по крестику (обычный)
        try:
            close_button = self.find_element(self.CLOSE_MODAL_BUTTON)
            print("   ✓ Крестик найден")
            close_button.click()
            print("   ✓ Обычный клик по крестику выполнен")
            self.wait.until(EC.invisibility_of_element_located(self.ORDER_MODAL))
            print("   ✓ Модальное окно закрыто")
            return
        except Exception as e:
            print(f"   ⚠ Обычный клик не сработал: {e}")
        
        # Способ 2: Клик по оверлею
        try:
            print("   🔧 Пробуем клик по оверлею...")
            overlay = self.find_element(self.MODAL_OVERLAY)
            overlay.click()
            print("   ✓ Клик по оверлею выполнен")
            self.wait.until(EC.invisibility_of_element_located(self.ORDER_MODAL))
            print("   ✓ Модальное окно закрыто")
            return
        except Exception as e:
            print(f"   ⚠ Клик по оверлею не сработал: {e}")
        
        # Способ 3: Клавиша ESC
        try:
            print("   🔧 Пробуем закрыть клавишей ESC...")
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)
            self.wait.until(EC.invisibility_of_element_located(self.ORDER_MODAL))
            print("   ✓ Модальное окно закрыто клавишей ESC")
            return
        except Exception as e:
            print(f"   ✗ Не удалось закрыть модальное окно: {e}")
            raise