import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class OrderFeedPage(BasePage):
    ALL_TIME_COUNTER = (By.XPATH, "//p[contains(text(),'Выполнено за всё время')]/following-sibling::p")
    TODAY_COUNTER = (By.XPATH, "//p[contains(text(),'Выполнено за сегодня')]/following-sibling::p")
    IN_PROGRESS_ORDERS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList__cBvyi')]/li")

    @allure.step("Получить счётчик 'За всё время'")
    def get_all_time_counter(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.ALL_TIME_COUNTER))
            element = self.find_element(self.ALL_TIME_COUNTER)
            value = int(element.text)
            print(f"   ✓ Счётчик 'За всё время': {value}")
            return value
        except:
            alt_locator = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderFeed__')]//p[contains(@class, 'text_type_digits-large')][1]")
            element = self.find_element(alt_locator)
            value = int(element.text)
            return value

    @allure.step("Получить счётчик 'За сегодня'")
    def get_today_counter(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.TODAY_COUNTER))
            element = self.find_element(self.TODAY_COUNTER)
            value = int(element.text)
            print(f"   ✓ Счётчик 'За сегодня': {value}")
            return value
        except:
            alt_locator = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderFeed__')]//p[contains(@class, 'text_type_digits-large')][2]")
            element = self.find_element(alt_locator)
            value = int(element.text)
            return value

    @allure.step("Проверить номер в работе")
    def is_order_in_progress(self, order_number):
        try:
            self.wait.until(lambda d: len(d.find_elements(*self.IN_PROGRESS_ORDERS)) > 0)
            time.sleep(1)
            orders = self.find_elements(self.IN_PROGRESS_ORDERS)
            numbers = [el.text.strip() for el in orders]
            print(f"   Номера в работе: {numbers}")
            
            # Проверяем, есть ли наш номер в списке (убираем ведущие нули для сравнения)
            clean_order = order_number.lstrip('0')
            for num in numbers:
                if num.lstrip('0') == clean_order:
                    print(f"   ✓ Номер {order_number} найден в списке")
                    return True
            
            print(f"   ✗ Номер {order_number} не найден в списке")
            return False
        except Exception as e:
            print(f"   ✗ Ошибка при проверке: {e}")
            return False