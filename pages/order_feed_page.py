import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    ALL_TIME_COUNTER = (By.XPATH, "//p[contains(text(),'Выполнено за всё время')]/following-sibling::p")
    TODAY_COUNTER = (By.XPATH, "//p[contains(text(),'Выполнено за сегодня')]/following-sibling::p")
    IN_PROGRESS_ORDERS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList__cBvyi')]/li")

    # Альтернативные локаторы
    ALT_ALL_TIME_COUNTER = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderFeed__')]//p[contains(@class, 'text_type_digits-large')]")

    @allure.step("Получить счётчик 'За всё время'")
    def get_all_time_counter(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.ALL_TIME_COUNTER))
            element = self.find_element(self.ALL_TIME_COUNTER)
            return int(element.text)
        except:
            elements = self.find_elements(self.ALT_ALL_TIME_COUNTER)
            return int(elements[0].text) if elements else 0

    @allure.step("Получить счётчик 'За сегодня'")
    def get_today_counter(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.TODAY_COUNTER))
            element = self.find_element(self.TODAY_COUNTER)
            return int(element.text)
        except:
            elements = self.find_elements(self.ALT_ALL_TIME_COUNTER)
            return int(elements[1].text) if len(elements) > 1 else 0

    @allure.step("Получить список номеров в работе")
    def get_orders_in_progress(self):
        self.wait.until(lambda d: len(d.find_elements(*self.IN_PROGRESS_ORDERS)) > 0)
        orders = self.find_elements(self.IN_PROGRESS_ORDERS)
        return [el.text.strip() for el in orders]

    @allure.step("Проверить номер {order_number} в работе")
    def is_order_in_progress(self, order_number):
        numbers = self.get_orders_in_progress()
        clean_order = order_number.lstrip('0')
        for num in numbers:
            if num.lstrip('0') == clean_order:
                return True
        return False