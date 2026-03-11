import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class IngredientModal(BasePage):
    MODAL = (By.XPATH, "//div[contains(@class, 'Modal') and contains(., 'Детали ингредиента')]")
    CLOSE_BUTTON = (By.XPATH, "//div[contains(@class, 'Modal')]//button")

    @allure.step("Проверить отображение модального окна")
    def is_displayed(self):
        try:
            self.find_element(self.MODAL)
            return True
        except:
            return False

    @allure.step("Закрыть модальное окно")
    def close(self):
        self.click(self.CLOSE_BUTTON)
        self.wait.until(EC.invisibility_of_element_located(self.MODAL))