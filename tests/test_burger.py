import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.ingredient_modal import IngredientModal
from pages.login_page import LoginPage
from utils.urls import Urls
from utils.data import TestData


@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.title("Тест 1: Переход на Конструктор")
    def test_constructor_navigation(self, driver):
        main_page = MainPage(driver)
        main_page.driver.get(Urls.BASE)

        main_page.click_order_feed()
        main_page.click_constructor()

        # Используем метод из BasePage
        assert main_page.get_current_url() == Urls.BASE

    @allure.title("Тест 2: Переход на Ленту заказов")
    def test_order_feed_navigation(self, driver):
        main_page = MainPage(driver)
        main_page.driver.get(Urls.BASE)

        main_page.click_order_feed()

        # Используем метод из BasePage
        assert "/feed" in main_page.get_current_url()

    @allure.title("Тест 3: Открытие/закрытие модального окна")
    def test_ingredient_modal_open_close(self, driver):
        main_page = MainPage(driver)
        main_page.driver.get(Urls.BASE)

        modal = IngredientModal(driver)
        main_page.click_ingredient(TestData.BUN_ALT)

        assert modal.is_displayed()

        modal.close()
        assert not modal.is_displayed()

    @allure.title("Тест 4: Увеличение счётчика на 2")
    def test_ingredient_counter_increases_by_two(self, driver):
        main_page = MainPage(driver)
        main_page.driver.get(Urls.BASE)

        before = main_page.get_ingredient_counter(TestData.BUN_ALT)
        after = main_page.add_ingredient_to_order(TestData.BUN_ALT)

        assert after == before + 2


@allure.feature("Лента заказов - проверка счётчиков")
class TestOrderFeedCounters:

    @allure.title("Тест 5.1: Счётчик 'За всё время' увеличивается после заказа")
    def test_all_time_counter_increases(self, driver, logged_in_user):
        main_page, feed_page = logged_in_user

        all_before = feed_page.get_all_time_counter()

        # Создание заказа
        main_page.click_constructor()
        main_page.add_ingredient_to_order(TestData.BUN_ALT)
        main_page.click_checkout()
        
        # Получаем номер заказа (ждем появления настоящего номера)
        order_number = main_page.get_order_number()
        
        # Закрываем модальное окно
        main_page.close_order_modal()

        # Проверка счётчика
        main_page.click_order_feed()
        all_after = feed_page.get_all_time_counter()

        assert all_after == all_before + 1

    @allure.title("Тест 5.2: Счётчик 'За сегодня' увеличивается после заказа")
    def test_today_counter_increases(self, driver, logged_in_user):
        main_page, feed_page = logged_in_user

        today_before = feed_page.get_today_counter()

        # Создание заказа
        main_page.click_constructor()
        main_page.add_ingredient_to_order(TestData.BUN_ALT)
        main_page.click_checkout()
        
        # Получаем номер заказа (ждем появления настоящего номера)
        order_number = main_page.get_order_number()
        
        # Закрываем модальное окно
        main_page.close_order_modal()

        # Проверка счётчика
        main_page.click_order_feed()
        today_after = feed_page.get_today_counter()

        assert today_after == today_before + 1


@allure.feature("Лента заказов - проверка номера в работе")
class TestOrderInProgress:

    @allure.title("Тест 5.3: Номер заказа появляется в разделе 'В работе'")
    def test_order_number_in_progress(self, driver, logged_in_user):
        main_page, feed_page = logged_in_user

        orders_before = feed_page.get_orders_in_progress()

        # Создание заказа
        main_page.click_constructor()
        main_page.add_ingredient_to_order(TestData.BUN_ALT)
        main_page.click_checkout()
        
        # Получаем номер заказа
        order_number = main_page.get_order_number()
        
        # Закрываем модальное окно
        main_page.close_order_modal()

        # Проверка наличия номера в работе
        main_page.click_order_feed()
        orders_after = feed_page.get_orders_in_progress()

        new_orders = [num for num in orders_after if num not in orders_before]
        assert len(new_orders) == 1, f"Ожидался 1 новый заказ, получено {len(new_orders)}"
        assert feed_page.is_order_in_progress(order_number), f"Номер {order_number} не найден в списке заказов"