import allure
import pytest
import time
from selenium.webdriver.common.by import By
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.ingredient_modal import IngredientModal
from pages.login_page import LoginPage

BASE_URL = "https://stellarburgers.education-services.ru/"
USER_EMAIL = "test2026@example.com"
USER_PASSWORD = "Qwerty123"
BUN_ALT = "Флюоресцентная булка R2-D3"


@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.title("Тест 1: Переход на Конструктор")
    def test_constructor_navigation(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        main_page.click_order_feed()
        main_page.click_constructor()
        assert driver.current_url in [BASE_URL, BASE_URL + "constructor"]

    @allure.title("Тест 2: Переход на Ленту заказов")
    def test_order_feed_navigation(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        main_page.click_order_feed()
        assert "/feed" in driver.current_url

    @allure.title("Тест 3: Открытие/закрытие модального окна")
    def test_ingredient_modal_open_close(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        modal = IngredientModal(driver)
        main_page.click_ingredient(BUN_ALT)
        assert modal.is_displayed()
        modal.close()
        assert not modal.is_displayed()

    @allure.title("Тест 4: Увеличение счётчика на 2")
    def test_ingredient_counter_increases_by_two(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)
        before = main_page.get_ingredient_counter(BUN_ALT)
        after = main_page.add_ingredient_to_order(BUN_ALT)
        assert after == before + 2


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Тест 5: Создание заказа - проверка счётчиков и появление номера в работе")
    def test_order_feed_counters_and_in_progress(self, driver):
        driver.get(BASE_URL)
        main_page = MainPage(driver)

        # ШАГ 1: Вход в аккаунт
        driver.get(BASE_URL + "login")
        time.sleep(2)
        login_page = LoginPage(driver)
        login_page.login(USER_EMAIL, USER_PASSWORD)

        # ШАГ 2: Переход в ленту заказов (счётчики ДО)
        main_page.click_order_feed()
        time.sleep(2)
        feed_page = OrderFeedPage(driver)

        orders_before = feed_page.find_elements(feed_page.IN_PROGRESS_ORDERS)
        numbers_before = [el.text.strip() for el in orders_before]

        all_before = feed_page.get_all_time_counter()
        today_before = feed_page.get_today_counter()

        # ШАГ 3: Создание заказа
        main_page.click_constructor()
        time.sleep(1)
        main_page.add_ingredient_to_order(BUN_ALT)
        main_page.click_checkout()
        time.sleep(2)

        # ШАГ 4: Закрытие модального окна
        main_page.close_order_modal()

        # ШАГ 5: Возврат в ленту заказов
        main_page.click_order_feed()
        time.sleep(3)

        # ШАГ 6: Проверка счётчиков ПОСЛЕ
        all_after = feed_page.get_all_time_counter()
        today_after = feed_page.get_today_counter()

        assert all_after == all_before + 1
        assert today_after == today_before + 1

        # ШАГ 7: Проверка появления нового заказа в разделе 'В работе'
        time.sleep(2)
        orders_after = feed_page.find_elements(feed_page.IN_PROGRESS_ORDERS)
        numbers_after = [el.text.strip() for el in orders_after]

        new_numbers = [num for num in numbers_after if num not in numbers_before]
        assert len(new_numbers) > 0, "Новый заказ не появился в разделе 'В работе'"